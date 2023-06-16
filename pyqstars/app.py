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
                for i in range(6):
                    rotation = piece.get_rotation(-60*i)
                    if board.has_place_at(rotation, row_i, col_i):
                        new_board = copy.deepcopy(board)
                        new_board.place(rotation, row_i, col_i)
                        new_pieces = [p for p in pieces if p is not piece]
                        solutions += solve(new_board, new_pieces)
                        break
    return solutions


def main() -> None:
    board = Board([
        ["g", "y", "y", "y", "r", "r", "-"],
        ["g", "y", "b", "r", "r", "-", "/"],
        ["-", "g", "g", "b", "p", "-", "p"],
        ["-", "-", "b", "b", "p", "p", "/"]
    ])
    # board = Board([
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["-", "-", "-", "-", "-", "-", "/"],
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["-", "-", "-", "-", "-", "-", "/"]
    # ])
    print("Finding solutions ...")
    solutions = solve(board, [PIECES["orange"], PIECES["violet"]])
    # solutions = solve(board, list(PIECES.values()))
    print(f"Result: found {len(solutions)} solutions!")
