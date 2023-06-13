from dataclasses import dataclass
from typing import Self

from pyqstars.core.hexagons import OddrOffsetCoordinate as Tile


@dataclass(frozen=True)
class Shape:
    """Composite of tiles."""
    id: str
    tiles: tuple[Tile]

    def get_matrix(self) -> list[list[bool]]:
        """TODO: docstring"""
        rows, cols = 7, 7
        matrix = [[False for _ in range(cols)] for _ in range(rows)]
        for hex in self.tiles:
            matrix[hex.row][hex.col] = True
        return matrix

    def rotated(self, center: Tile, degree: int = 60) -> Self:
        """Returns a clockwise-rotated copy of this object.

        Args:
            center: The center to rotate around.
            degree: The degree of rotation. Must be a positive multiple of 60.
        """
        tiles = tuple(tile.rotated(center, degree) for tile in self.tiles)
        return type(self)(self.id, tiles)

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
