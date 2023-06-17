from datetime import datetime
from timeit import default_timer as timer
from typing import Iterable

from pyqstars.board import Board, Piece, Tile

PIECES = {
    "blue": Piece("b", [Tile(0, 0), Tile(1, 0), Tile(2, 0), Tile(1, 1)]),
    "green": Piece("g", [Tile(0, 0), Tile(1, 0), Tile(1, 1), Tile(2, 2)]),
    "orange": Piece("o", [Tile(0, 0), Tile(1, 0), Tile(1, 1)]),
    "pink": Piece("p", [Tile(0, 0), Tile(1, 0), Tile(1, 1), Tile(1, 2)]),
    "red": Piece("r", [Tile(0, 0), Tile(1, 0), Tile(0, 1), Tile(1, 1)]),
    "violet": Piece("v", [Tile(0, 0), Tile(1, 0), Tile(2, 0)]),
    "yellow": Piece("y", [Tile(0, 0), Tile(1, 0), Tile(2, 0), Tile(0, 1)])
}


def inspect(objs: Iterable[object]) -> None:
    """Prints a pretty overview of the given Iterable."""
    separator = "\n\n# ---------------------------------------------- #\n\n"
    print(
        "\n",
        separator.join(str(obj) for obj in objs),
        "\n",
        sep=""
    )
    return None


def unique(boards: list[Board]) -> list[Board]:
    """Returns unique combinations.

    Args:
        boards: Combinations to filter.
    """
    unique_boards: list[Board] = []
    for board in boards:
        if not unique_boards:
            unique_boards.append(board)
            continue
        is_unique = all(
            any(
                unique_board.matrix[row][col] != board.matrix[row][col]
                for row, col in Board.get_fields()
            )
            for unique_board in unique_boards
        )
        if is_unique:
            unique_boards.append(board)
    return unique_boards


def solve(board: Board, pieces: list[Piece]) -> list[Board]:
    """Returns all possible combinations.

    Args:
        board: The board to place pieces on.
        pieces: The pieces to place on the board.
    """
    if not pieces:
        return [board]
    solutions: list[Board] = []
    for piece in pieces:
        for row, col in Board.get_fields():
            if (new_board := board.place(piece, row, col)) is not None:
                new_pieces = [p for p in pieces if p.id != piece.id]
                solutions += solve(new_board, new_pieces)
    return solutions


def main() -> None:
    board = Board([
        ["-", "-", "-", "v", "v", "v", "o"],
        ["-", "-", "-", "-", "-", "o", "/"],
        ["-", "-", "-", "-", "-", "-", "o"],
        ["-", "-", "-", "-", "-", "-", "/"]
    ])
    pieces = [
        PIECES["blue"],
        PIECES["green"],
        PIECES["pink"],
        PIECES["red"],
        PIECES["yellow"]
    ]
    pieces = [r for p in pieces for r in p.get_unique_rotations()]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Finding solutions ...")
    start = timer()
    combinations = solve(board, pieces)
    solutions = unique(combinations)
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] Result:",
        f"  run time      : {timer()-start}"
        f"  combination(s): {len(combinations)}",
        f"  solutions(s)  : {len(solutions)}",
        sep="\n"
    )
    inspect(solutions)
    return None
