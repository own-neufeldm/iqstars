# Reference: https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, init=False)
class Cube():
    """Cube coordinate.

    All operations within this library are effectively done via this class."""
    _DIRECTION_VECTORS = {
        "e": (+1, 0, -1),
        "ne": (+1, -1, 0),
        "nw": (0, -1, +1),
        "w": (-1, 0, +1),
        "sw": (-1, +1, 0),
        "se": (0, +1, -1)
    }
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
    def from_oddr(cls, offset: "OddRowedOffset") -> Self:
        """Constructs from an odd-rowed offset coordinate."""
        q = offset.col - (offset.row - (offset.row % 2)) // 2
        r = offset.row
        return cls(q, r)

    def get_neighbor(self, direction: str) -> Self:
        """"Returns a neighbor.

        Args:
            direction: Compass direction, one of [e, ne, nw, w, sw, se]
        """
        return self + Cube(*Cube._DIRECTION_VECTORS[direction])

    def _get_rotation(self, degree: int) -> Self:
        q, r, s = self.q, self.r, self.s
        times = degree // 60
        if times < 0:
            for _ in range(abs(times)):
                q, r, s = -r, -s, -q
        else:
            for _ in range(times):
                q, r, s = -s, -q, -r
        return type(self)(q, r)

    def get_rotation(self, center: Self, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        if degree % 60 != 0:
            raise ValueError(f"degree ({degree}) must be a multiple of 60.")
        if degree == 0:
            return type(self)(self.q, self.r)
        vector = self - center
        return vector._get_rotation(degree)


@dataclass(frozen=True)
class OddRowedOffset():
    """Odd-rowed offset coordinate.

    Serves as simplified API for performing operations in a hexagonal grid."""
    col: int
    row: int

    def __add__(self, other: Self) -> Self:
        return type(self).from_cube(
            Cube.from_oddr(self) + Cube.from_oddr(other)
        )

    def __sub__(self, other: Self) -> Self:
        return type(self).from_cube(
            Cube.from_oddr(self) - Cube.from_oddr(other)
        )

    @classmethod
    def from_cube(cls, cube: "Cube") -> Self:
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
            Cube.from_oddr(self).get_neighbor(direction)
        )

    def get_rotation(self, center: Self, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        return type(self).from_cube(
            Cube.from_oddr(self).get_rotation(
                Cube.from_oddr(center), degree
            )
        )
