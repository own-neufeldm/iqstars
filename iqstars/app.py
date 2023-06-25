from datetime import datetime
from timeit import default_timer as timer
from typing import Iterable

from iqstars.board import Board, Piece, Tile

PIECES = {
    "blue": Piece("b", [Tile(0, 0), Tile(1, 0), Tile(2, 0), Tile(1, 1)]),
    "green": Piece("g", [Tile(0, 0), Tile(1, 0), Tile(1, 1), Tile(2, 2)]),
    "orange": Piece("o", [Tile(0, 0), Tile(1, 0), Tile(1, 1)]),
    "pink": Piece("p", [Tile(0, 0), Tile(1, 0), Tile(1, 1), Tile(1, 2)]),
    "red": Piece("r", [Tile(0, 0), Tile(1, 0), Tile(0, 1), Tile(1, 1)]),
    "violet": Piece("v", [Tile(0, 0), Tile(1, 0), Tile(2, 0)]),
    "yellow": Piece("y", [Tile(0, 0), Tile(1, 0), Tile(2, 0), Tile(0, 1)])
}


def _inspect(objs: Iterable[object]) -> None:
    """Prints a pretty overview of the given Iterable."""
    separator = "\n\n# ---------------------------------------------- #\n\n"
    print(
        "\n",
        separator.join(str(obj) for obj in objs),
        "\n",
        sep=""
    )
    return None


def _unique(boards: list[Board]) -> list[Board]:
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


def _solve(board: Board, pieces: list[Piece]) -> list[Board]:
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
                solutions += _solve(new_board, new_pieces)
    return solutions


def solve(board: Board, pieces: list[Piece]) -> None:
    """Solves the given board by inserting the given pieces."""
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] Finding solutions for:",
        "",
        board,
        "",
        sep="\n"
    )
    start = timer()
    combinations = _solve(board, pieces)
    solutions = _unique(combinations)
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] Result:",
        f"  run time       : {timer()-start:.3f}s",
        f"  combination(s) : {len(combinations)}",
        f"  solutions(s)   : {len(solutions)}",
        sep="\n"
    )
    _inspect(solutions)
    return None
