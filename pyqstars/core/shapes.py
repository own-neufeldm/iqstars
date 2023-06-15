from dataclasses import dataclass
from typing import Self

from pyqstars.core.hexlib import OddRowedOffset as Tile


@dataclass(frozen=True, init=False)
class Shape:
    """Composite of coordinates (tiles) in an odd-rowed offset system."""
    id: str
    tiles: tuple[Tile, ...]

    def __init__(self, id: str, tiles: tuple[Tile, ...]) -> None:
        if len(tiles) < 2:
            raise ValueError(f"tiles ({tiles}) must be longer than 1.")
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "tiles", _normalized(tiles))
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

    def get_matrix(self) -> list[list[bool]]:
        """Mapping of tiles in a grid, True if occupied."""
        size = 4  # hard-coded because all shapes used as of now fit in here
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


def _normalized(tiles: tuple[Tile]) -> tuple[Tile]:
    # move to smallest possible row >= 0
    if min(t.row for t in tiles) < 0:
        while min(t.row for t in tiles) < 0:
            tiles = tuple(t.get_neighbor("se") for t in tiles)
    else:
        while min(t.row for t in tiles) > 0:
            tiles = tuple(t.get_neighbor("nw") for t in tiles)
    # move to col 0
    while min(t.col for t in tiles) < 0:
        tiles = tuple(t.get_neighbor("e") for t in tiles)
    while min(t.col for t in tiles) > 0:
        tiles = tuple(t.get_neighbor("w") for t in tiles)
    # # adjust to even row
    # in_even_row = False
    # for tile in (t for t in tiles if t.col == 0):
    #     if tile.row % 2 == 0:
    #         in_even_row = True
    #         break
    # if not in_even_row:
    #     tiles = tuple(t.get_neighbor("sw") for t in tiles)
    return tiles
