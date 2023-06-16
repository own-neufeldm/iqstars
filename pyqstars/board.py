from dataclasses import dataclass
from typing import Self

from pyqstars.hexlib import OddRowedOffset as Tile

SIZE_COL = 7
SIZE_ROW = 4


@dataclass(frozen=True, init=False)
class Piece:
    """Puzzle piece."""
    id: str
    tiles: list[Tile]

    def __init__(self, id: str, tiles: list[Tile]) -> None:
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "tiles", self._normalized(tiles))
        return None

    def __str__(self) -> str:
        unoccupied, occupied = "-", self.id
        lines: list[str] = []
        for row_i, row in enumerate(self.get_matrix()):
            line: list[str] = [""] if row_i % 2 != 0 else []
            for col in row:
                line.append(occupied if col else unoccupied)
            lines.append(" ".join(line))
        return "\n".join(lines)

    def _normalized(self, tiles: list[Tile]) -> list[Tile]:
        """Shifts all tiles to the smallest positive position possible."""
        while min(t.row for t in tiles) < 0:
            tiles = [t.get_neighbor("se") for t in tiles]
        while min(t.row for t in tiles) > 0:
            tiles = [t.get_neighbor("nw") for t in tiles]
        while min(t.col for t in tiles) < 0:
            tiles = [t.get_neighbor("e") for t in tiles]
        while min(t.col for t in tiles) > 0:
            tiles = [t.get_neighbor("w") for t in tiles]
        return tiles

    def get_matrix(self) -> list[list[bool]]:
        """Returns a 2D mapping of the tiles, True if occupied."""
        size = min(SIZE_COL, SIZE_ROW)
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
        return type(self)(
            self.id,
            [tile.get_rotation(center, degree) for tile in self.tiles]
        )


@dataclass(frozen=True)
class Board:
    """Game board."""
    matrix: list[list[str]]
