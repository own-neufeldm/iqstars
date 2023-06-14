# https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
from typing import Self, Type


@dataclass(order=True)
class Cube():
    """Cube coordinate for performing complex operations in a hexagonal grid."""
    q: int
    r: int
    s: int

    @classmethod
    def get_direction_vectors(cls) -> tuple[Self]:
        """Precomputed permutations for neighbors."""
        return (
            cls(+1, 0, -1), cls(+1, -1, 0), cls(0, -1, +1),
            cls(-1, 0, +1), cls(-1, +1, 0), cls(0, +1, -1),
        )

    @classmethod
    def from_oddr(cls, offset: Type["OddRowedOffset"]) -> Self:
        """Constructs from an odd-rowed offset coordinate."""
        q = offset.q - (offset.r - (abs(offset.r) % 2)) // 2
        r = offset.r
        return cls(q, r, -q-r)

    def __add__(self, other: Self) -> Self:
        return type(self)(
            self.q + other.q,
            self.r + other.r,
            self.s + other.s
        )

    def __sub__(self, other: Self) -> Self:
        return type(self)(
            self.q - other.q,
            self.r - other.r,
            self.s - other.s
        )

    def moved(self, neighbor: int) -> Self:
        """"Returns a moved copy of this object.

        Args:
            neighbor: The neighbor to move to, starting from 0 as right neighbor
            and increasing counterclockwise to 5.
        """
        return self + type(self).get_direction_vectors()[neighbor]

    def rotated(self, degree: int = 60) -> Self:
        """Returns a clockwise-rotated copy of this object.

        Args:
            degree: The degree of rotation. Must be a positive multiple of 60.
        """
        if degree < 0 or degree % 60 != 0:
            raise ValueError(
                f"Degree of rotation must be a positive multiple of 60, "
                f"is {degree}."
            )
        q, r, s = self.q, self.r, self.s
        for _ in range(degree // 60):
            q, r, s = -r, -s, -q
        return type(self)(q, r, s)


@dataclass(order=True)
class OddRowedOffset():
    """Coordinate in an odd-rowed offset system."""
    q: int
    r: int

    @classmethod
    def from_cube(cls, cube: Type["Cube"]) -> Self:
        """Constructs from a cube coordinate."""
        col = cube.q + (cube.r - (abs(cube.r) % 2)) // 2
        row = cube.r
        return cls(col, row)

    def moved(self, neighbor: int) -> Self:
        """"Returns a moved copy of this object.

        Args:
            neighbor: The neighbor to move to, starting from 0 as right neighbor
            and increasing counterclockwise to 5.
        """
        return type(self).from_cube(
            Cube.from_oddr(self).moved(neighbor)
        )

    def rotated(self, center: Self, degree: int = 60) -> Self:
        """Returns a clockwise-rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Must be a positive multiple of 60.
        """
        center_cube = Cube.from_oddr(center)
        vector_cube = Cube.from_oddr(self) - center_cube
        rotated_cube = vector_cube.rotated(degree) + center_cube
        return type(self).from_cube(rotated_cube)
