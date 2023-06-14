from dataclasses import dataclass
from typing import Self

from pyqstars.core.hexlib import OddRowedOffset as Tile


@dataclass(frozen=True, init=False)
class Shape:
    """Composite of coordinates (tiles) in an odd-rowed offset system."""
    id: str
    tiles: tuple[Tile]

    def __init__(self, id: str, tiles: tuple[Tile]) -> None:
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "tiles", self._normalized(tiles))
        return None

    def __str__(self) -> str:
        unoccupied, occupied = "-", "*"
        lines: list[str] = []
        for row_i, row in enumerate(self.get_matrix()):
            line: list[str] = []
            for col in row:
                line.append(occupied if col else unoccupied)
            string = " ".join(line)
            if row_i % 2 == 1:
                string = " " + string
            lines.append(string)
        return "\n".join(lines)

    def _normalized(self, tiles: tuple[Tile]) -> tuple[Tile]:
        row_off = min(tile.row for tile in tiles)
        if row_off % 2 != 0:
            tiles = tuple(tile.get_neighbor("nw") for tile in tiles)
            row_off = row_off - 1
        col_off = min([tile.col for tile in tiles])
        if col_off == 0 and row_off == 0:
            return tiles
        for tile in tiles:
            tile.col = tile.col - col_off
            tile.row = tile.row - row_off
        return tiles

    def get_matrix(self) -> list[list[bool]]:
        """Mapping of tiles in a grid, True if occupied."""
        size = 4
        matrix = [[False for _ in range(size)] for _ in range(size)]
        for tile in self.tiles:
            matrix[tile.row][tile.col] = True
        return matrix

    def get_rotation(self, center: Tile, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        tiles = tuple(tile.get_rotation(center, degree) for tile in self.tiles)
        return type(self)(self.id, tiles)
