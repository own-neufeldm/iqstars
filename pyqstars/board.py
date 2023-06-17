import copy
import itertools
from dataclasses import dataclass
from typing import Iterable, Self

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

    def get_unique_rotations(self) -> list[Self]:
        """Returns a list of unique rotations for this object."""
        unique_rotations: list[Self] = []
        for rotation in [self.get_rotation(-60*i) for i in range(6)]:
            if not unique_rotations:
                unique_rotations.append(rotation)
                continue
            is_unique = all(
                any(
                    tile not in unique_rotation.tiles
                    for tile in rotation.tiles
                )
                for unique_rotation in unique_rotations
            )
            if is_unique:
                unique_rotations.append(rotation)
        return unique_rotations


@dataclass(frozen=True, init=False)
class Board:
    """Game board."""
    matrix: list[list[str]]

    def __init__(self, matrix: list[list[str]] | None = None) -> None:
        if matrix is None:
            matrix = [
                [UNOCCUPIED for _ in range(SIZE_COL)]
                if i % 2 == 0 else
                [UNOCCUPIED for _ in range(SIZE_COL-1)] + [UNAVAILABLE]
                for i in range(SIZE_ROW)
            ]
        elif any(
            len(matrix) != SIZE_ROW or
            len(row) != SIZE_COL for row in matrix
        ):
            raise ValueError(
                f"Matrix does not meet size requirements. "
                f"Must have {SIZE_ROW} rows with {SIZE_COL} each."
            )
        object.__setattr__(self, "matrix",  matrix)
        return None

    def __str__(self) -> str:
        unavailable = UNAVAILABLE
        lines: list[str] = []
        for row_i, row in enumerate(self.matrix):
            line = [""] if row_i % 2 != 0 else []
            line += [col for col in row if col != unavailable]
            lines.append(" ".join(line))
        return ("\n".join(lines))

    @classmethod
    def get_fields(cls) -> Iterable[tuple[int, int]]:
        """Returns an iterable of (row, col) indices for fields of any Board."""
        return itertools.product(range(SIZE_ROW), range(SIZE_COL))

    def place(self, piece: Piece, row: int, col: int) -> Self | None:
        """Returns a copy of this object with the given piece placed.

        If the piece cannot be placed, None will be returned."""
        new_board = copy.deepcopy(self)
        target = Tile(col, row)
        for tile in piece.tiles:
            vector = piece.get_vector(tile, target)
            is_out_of_range = (
                vector.col < 0 or vector.col > SIZE_COL-1
                or vector.row < 0 or vector.row > SIZE_ROW-1
            )
            if is_out_of_range:
                return None
            if new_board.matrix[vector.row][vector.col] == UNOCCUPIED:
                new_board.matrix[vector.row][vector.col] = piece.id
            else:
                return None
        return new_board
