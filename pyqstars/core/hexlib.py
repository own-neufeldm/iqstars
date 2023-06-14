# https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
from typing import Self, Type


@dataclass(frozen=True, order=True)
class Cube():
    """Cube coordinate for performing complex operations in a hexagonal grid."""
    q: int
    r: int
    s: int = None

    def __post_init__(self) -> None:
        if self.s is None:
            object.__setattr__(self, "s", -self.q-self.r)
        return None

    def __add__(self, other: Self) -> Self:
        return type(self)(self.q + other.q, self.r + other.r)

    def __sub__(self, other: Self) -> Self:
        return type(self)(self.q - other.q, self.r - other.r)

    @classmethod
    def get_direction_vectors(cls) -> dict[str, Self]:
        """Precomputed permutations for neighbors, direction to vector."""
        return {
            "e": cls(+1, 0, -1),
            "ne": cls(+1, -1, 0),
            "nw": cls(0, -1, +1),
            "w": cls(-1, 0, +1),
            "sw": cls(-1, +1, 0),
            "se": cls(0, +1, -1)
        }

    @classmethod
    def from_oddr(cls, offset: Type["OddRowedOffset"]) -> Self:
        """Constructs from an odd-rowed offset coordinate."""
        q = offset.col - (offset.row - (abs(offset.row) % 2)) // 2
        r = offset.row
        return cls(q, r)

    def get_neighbor(self, direction: str) -> Self:
        """"Returns a neighbor.

        Args:
            direction: Compass direction, one of [e, ne, nw, w, sw, se]
        """
        return self + type(self).get_direction_vectors()[direction]

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


@dataclass(order=True)
class OddRowedOffset():
    """Coordinate in an odd-rowed offset system."""
    col: int
    row: int

    @classmethod
    def from_cube(cls, cube: Type["Cube"]) -> Self:
        """Constructs from a cube coordinate."""
        col = cube.q + (cube.r - (abs(cube.r) % 2)) // 2
        row = cube.r
        return cls(col, row)

    def get_neighbor(self, direction: str) -> Self:
        """"Returns a neighbor.

        Args:
            direction: Compass direction, one of [e, ne, nw, w, sw, se]
        """
        return type(self).from_cube(
            Cube.from_oddr(self).get_neighbor(direction)
        )

    def get_rotation(self, center: Self, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        center_cube = Cube.from_oddr(center)
        vector_cube = Cube.from_oddr(self) - center_cube
        rotated_cube = vector_cube.get_rotation(degree) + center_cube
        return type(self).from_cube(rotated_cube)
