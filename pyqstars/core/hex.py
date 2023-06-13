# https://www.redblobgames.com/grids/hexagons/

from dataclasses import dataclass
from typing import Self, Type


@dataclass
class Cube():
    col: int
    row: int
    spc: int

    @classmethod
    def coordinates_from_hex(cls, hex: Type["Hex"]) -> tuple[int, int, int]:
        col = hex.col - (hex.row - (abs(hex.row) % 2)) // 2
        row = hex.row
        return (col, row, -col-row)

    @classmethod
    def from_hex(cls, hex: Type["Hex"]) -> Self:
        return cls(*cls.coordinates_from_hex(hex))

    def rotate(self) -> None:
        self.col, self.row, self.spc = -self.row, -self.spc, -self.col
        return None


@dataclass
class Hex():
    col: int
    row: int

    @classmethod
    def coordinates_from_cube(cls, cube: Type["Cube"]) -> tuple[int, int]:
        col = cube.col + (cube.row - (abs(cube.row) % 2)) // 2
        row = cube.row
        return (col, row)

    @classmethod
    def from_cube(cls, cube: Type["Cube"]) -> Self:
        return cls(*cls.coordinates_from_cube(cube))

    def rotate(self, center: Self) -> None:
        center_cube = Cube.from_hex(center)
        self_cube = Cube.from_hex(self)
        vector = Cube(
            self_cube.col - center_cube.col,
            self_cube.row - center_cube.row,
            self_cube.spc - center_cube.spc
        )
        vector.rotate()
        rotated_cube = Cube(
            vector.col + center_cube.col,
            vector.row + center_cube.row,
            vector.spc + center_cube.spc
        )
        self.col, self.row = type(self).coordinates_from_cube(rotated_cube)
        return None
