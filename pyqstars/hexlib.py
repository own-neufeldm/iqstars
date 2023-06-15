# https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
from typing import Self, Type


@dataclass(frozen=True, init=False)
class Cube():
    """Cube coordinate for performing complex operations in a hexagonal grid."""
    q: int
    r: int
    s: int

    def __init__(self, q: int, r: int, s: int | None = None) -> None:
        if s is None:
            s = -q-r
        object.__setattr__(self, "q", q)
        object.__setattr__(self, "r", r)
        object.__setattr__(self, "s", s)
        return None

    def __post_init__(self) -> None:
        if self.s is None:
            object.__setattr__(self, "s", -self.q-self.r)
        return None

    def __add__(self, other: Self) -> Self:
        return type(self)(self.q + other.q, self.r + other.r)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.q - other.q, self.r - other.r)

    @classmethod
    def from_oddr(cls, offset: Type["OddRowedOffset"]) -> Self:
        """Constructs from an odd-rowed offset coordinate."""
        q = offset.col - (offset.row - (offset.row % 2)) // 2
        r = offset.row
        return cls(q, r)

    def get_neighbor(self, direction: str) -> Self:
        """"Returns a neighbor.

        Args:
            direction: Compass direction, one of [e, ne, nw, w, sw, se]
        """
        return self + CUBE_DIRECTION_VECTORS[direction]

    def get_rotation(self, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        if degree % 60 != 0:
            raise ValueError(f"degree ({degree}) must be a multiple of 60.")
        if degree == 0:
            return type(self)(self.q, self.r)
        q, r, s = self.q, self.r, self.s
        times = degree // 60
        if times < 0:
            for _ in range(abs(times)):
                q, r, s = -r, -s, -q
        else:
            for _ in range(times):
                q, r, s = -s, -q, -r
        return type(self)(q, r)


@dataclass(frozen=True)
class OddRowedOffset():
    """Coordinate in an odd-rowed offset system."""
    col: int
    row: int

    @classmethod
    def from_cube(cls, cube: Type["Cube"]) -> Self:
        """Constructs from a cube coordinate."""
        col = cube.q + (cube.r - (cube.r % 2)) // 2
        row = cube.r
        return cls(col, row)

    def get_neighbor(self, direction: str) -> Self:
        """"Returns a neighbor.

        Args:
            direction: Compass direction, one of [e, ne, nw, w, sw, se]
        """
        return type(self).from_cube(
            Cube.from_oddr(self).get_neighbor(direction)  # type: ignore
        )

    def get_rotation(self, center: Self, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        center_cube = Cube.from_oddr(center)  # type: ignore
        vector_cube = Cube.from_oddr(self) - center_cube  # type: ignore
        rotated_cube = vector_cube.get_rotation(degree) + center_cube
        return type(self).from_cube(rotated_cube)  # type: ignore


CUBE_DIRECTION_VECTORS = {
    "e": Cube(+1, 0, -1),
    "ne": Cube(+1, -1, 0),
    "nw": Cube(0, -1, +1),
    "w": Cube(-1, 0, +1),
    "sw": Cube(-1, +1, 0),
    "se": Cube(0, +1, -1)
}
