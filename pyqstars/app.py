import copy
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


def inspect(shapes: Iterable[Piece]) -> None:
    separator = "\n\n# ---------------------------------------------- #\n\n"
    print(
        "\n",
        separator.join(f"{piece!r}\n\n{piece!s}" for piece in shapes),
        "\n",
        sep=""
    )


def solve(board: Board, pieces: list[Piece]) -> list[Board]:
    if not pieces:
        return [board]
    solutions: list[Board] = []
    for row_i, row in enumerate(board.matrix):
        for col_i, _ in enumerate(row):
            for piece in pieces:
                for rotation in piece.get_unique_rotations():
                    if board.has_place_at(rotation, row_i, col_i):
                        new_board = copy.deepcopy(board)
                        new_board.place(rotation, row_i, col_i)
                        new_pieces = [p for p in pieces if p is not piece]
                        solutions += solve(new_board, new_pieces)
                        break
    return solutions


def main() -> None:
    from timeit import default_timer as timer
    board = Board([
        ["g", "y", "y", "y", "-", "-", "-"],
        ["g", "y", "-", "-", "-", "-", "/"],
        ["-", "g", "g", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "/"]
    ])
    pieces = [
        PIECES["blue"],
        PIECES["orange"],
        PIECES["pink"],
        PIECES["red"],
        PIECES["violet"]
    ]
    print("Finding solutions ...")
    start = timer()
    solutions = solve(board, pieces)
    end = timer()
    print(f"Result: found {len(solutions)} solutions in {end-start:.2f}s!")
    return None
