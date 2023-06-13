# https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
from typing import Self, Type


@dataclass
class _Cube():
    """Cube coordinate for performing complex operations in a hexagonal grid."""
    col: int
    row: int
    spc: int

    @classmethod
    def from_oddr_oc(cls, coord: Type["OddrOffsetCoordinate"]) -> Self:
        """Constructs from an odd-rowed offset coordinate."""
        col = coord.col - (coord.row - (abs(coord.row) % 2)) // 2
        row = coord.row
        return cls(col, row, -col-row)

    def __add__(self, other: Self) -> Self:
        return type(self)(
            self.col + other.col,
            self.row + other.row,
            self.spc + other.spc
        )

    def __sub__(self, other: Self) -> Self:
        return type(self)(
            self.col - other.col,
            self.row - other.row,
            self.spc - other.spc
        )

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
        col, row, spc = self.col, self.row, self.spc
        for _ in range(degree // 60):
            col, row, spc = -row, -spc, -col
        return type(self)(col, row, spc)


@dataclass
class OddrOffsetCoordinate():
    """Coordinate in an odd-rowed offset system."""
    col: int
    row: int

    @classmethod
    def from_cube(cls, cube: Type["_Cube"]) -> Self:
        """Constructs from a cube."""
        col = cube.col + (cube.row - (abs(cube.row) % 2)) // 2
        row = cube.row
        return cls(col, row)

    # def _update(self, new: Self) -> None:
    #     self.col, self.row = new.col, new.row
    #     return None

    def rotated(self, center: Self, degree: int = 60) -> Self:
        """Returns a clockwise-rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Must be a positive multiple of 60.
        """
        center_cube = _Cube.from_oddr_oc(center)
        vector_cube = _Cube.from_oddr_oc(self) - center_cube
        rotated_cube = vector_cube.rotated(degree) + center_cube
        rotated_self = type(self).from_cube(rotated_cube)
        return type(self)(rotated_self.col, rotated_self.row)
