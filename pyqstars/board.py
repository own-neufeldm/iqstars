import logging
from dataclasses import dataclass
from typing import Self

from pyqstars.hexlib import OddRowedOffset as Tile

SIZE_COL = 7
SIZE_ROW = 4
UNOCCUPIED = "-"
UNAVAILABLE = "/"


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
        unoccupied, occupied = UNOCCUPIED, self.id
        lines: list[str] = []
        for row_i, row in enumerate(self.get_matrix()):
            line = [""] if row_i % 2 != 0 else []
            line += [occupied if col else unoccupied for col in row]
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

    def get_center(self) -> Tile:
        """Returns the center tile of this object."""
        return self.tiles[0]  # xD

    def get_vector(self, tile: Tile, target: Tile) -> Tile:
        """Returns the vector from the given tile to the given target."""
        return target + tile - self.get_center()

    def get_matrix(self) -> list[list[bool]]:
        """Returns a 2D mapping of the tiles, True if occupied."""
        size = min(SIZE_COL, SIZE_ROW)
        matrix = [[False for _ in range(size)] for _ in range(size)]
        for tile in self.tiles:
            matrix[tile.row][tile.col] = True
        return matrix

    def get_rotation(self, degree: int = -60) -> Self:
        """Returns a rotated copy of this object.

        Args:
            degree: The degree of rotation. Default is one rotation clockwise.
        """
        return type(self)(
            self.id,
            [
                tile.get_rotation(self.get_center(), degree)
                for tile in self.tiles
            ]
        )


@dataclass(frozen=True)
class Board:
    """Game board."""
    matrix: list[list[str]]

    def __str__(self) -> str:
        unavailable = UNAVAILABLE
        lines: list[str] = []
        for row_i, row in enumerate(self.matrix):
            line = [""] if row_i % 2 != 0 else []
            line += [col for col in row if col != unavailable]
            lines.append(" ".join(line))
        return ("\n".join(lines))

    def has_place_at(self, piece: Piece, row: int, col: int) -> bool:
        """Checks if the given piece fits at the given position."""
        target = Tile(col, row)
        for tile in piece.tiles:
            vector = piece.get_vector(tile, target)
            logging.debug(
                f"Checking if board has place:\n"
                f"  piece  : {piece!r}\n\n{piece!s}\n\n"
                f"  tile   : {tile}\n"
                f"  target : {target}\n"
                f"  vector : {vector}\n"
                f"  board  : <see below>\n\n{self}\n"
            )
            # input("\nPress Return to continue ...\n")
            if vector.col < 0 or vector.row < 0:
                logging.debug("Vector col and/or row < 0, aborting!")
                # input("\nPress Return to continue ...\n")
                return False
            try:
                has_place = self.matrix[vector.row][vector.col] == UNOCCUPIED
            except IndexError:
                logging.debug("IndexError, aborting!")
                # input("\nPress Return to continue ...\n")
                return False
            else:
                if not has_place:
                    logging.debug("Place already occupied, aborting!")
                    # input("\nPress Return to continue ...\n")
                    return False
        logging.debug("Place unoccupied!")
        # input("\nPress Return to continue ...\n")
        return True

    def place(self, piece: Piece, row: int, col: int) -> None:
        """Places the given piece at the given location."""
        target = Tile(col, row)
        for tile in piece.tiles:
            vector = piece.get_vector(tile, target)
            self.matrix[vector.row][vector.col] = piece.id
        return None
