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
    solutions: list[Board] = []
    return solutions


def main() -> None:
    # board = Board([
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["-", "-", "-", "-", "-", "-", "/"],
    #     ["-", "-", "-", "-", "-", "-", "-"],
    #     ["-", "-", "-", "-", "-", "-", "/"]
    # ])
    # logging.info("Finding solutions ...")
    # solutions = solve(board, list(SHAPES.values()))
    # logging.info(f"Result: found {solutions} solutions!")
    for piece in PIECES.values():
        inspect([
            piece.get_rotation(piece.tiles[0], -60*i)
            for i in range(6)
        ])
    return None


# def dumps(board: list[list[str]]) -> str:
#     lines: list[str] = []
#     for row_i, row in enumerate(board):
#         line = [col for col in row]
#         if row_i % 2 != 0:
#             line.insert(0, "")
#         lines.append(" ".join(line))
#     return ("\n".join(lines))


# def dump(board: list[list[str]]) -> None:
#     print(dumps(board))


# def place(board: list[list[str]], shape: Piece, row: int, col: int) -> None:
#     place_oddr = Tile(col, row)
#     place_cube = Cube.from_oddr(place_oddr)  # type: ignore
#     center_oddr = shape.tiles[0]
#     center_cube = Cube.from_oddr(center_oddr)  # type: ignore
#     for tile in shape.tiles:
#         tile_cube = Cube.from_oddr(tile)  # type: ignore
#         vector_cube = place_cube + tile_cube - center_cube
#         vector_oddr = Tile.from_cube(vector_cube)  # type: ignore
#         board[vector_oddr.row][vector_oddr.col] = shape.id
#     return None


# def has_place(board: list[list[str]], shape: Piece, row: int, col: int) -> bool:
#     place_oddr = Tile(col, row)
#     place_cube = Cube.from_oddr(place_oddr)  # type: ignore
#     center_oddr = shape.tiles[0]
#     center_cube = Cube.from_oddr(center_oddr)  # type: ignore
#     for tile in shape.tiles:
#         tile_cube = Cube.from_oddr(tile)  # type: ignore
#         vector_cube = place_cube + tile_cube - center_cube
#         vector_oddr = Tile.from_cube(vector_cube)  # type: ignore
#         logging.debug(
#             f"Checking if board has place:\n"
#             f"  shape        : {shape!r}\n"
#             f"  tile         : {tile}\n"
#             f"  center index : ({col=}, {row=})\n"
#             f"  vector index : (col={vector_oddr.col}, row={vector_oddr.row})\n"
#             f"  board : <see below>\n\n{dumps(board)}"
#         )
#         if vector_oddr.col < 0 or vector_oddr.row < 0:
#             logging.debug("This tile does not fit, aborting.\n\n")
#             return False
#         try:
#             if board[vector_oddr.row][vector_oddr.col] != "-":
#                 logging.debug("This tile does not fit, aborting.\n\n")
#                 return False
#         except IndexError:
#             logging.debug("This tile does not fit, aborting.\n\n")
#             return False
#         logging.debug("This tile fits.\n\n")
#     logging.debug("All tiles fit.\n\n")
#     return True


# def solve(board: list[list[str]], shapes: Iterable[Shape]) -> Iterable[list[list[str]]]:
#     solutions: list[list[list[str]]] = []
#     ...
#     return solutions
#     shapes = list(shapes)
#     if not shapes:
#         global solved_boards
#         solved_boards.append(board)
#         logging.info("Solved following board:")
#         dump(board)
#         return True
#     for shape in shapes:
#         center = shape.tiles[0]
#         rotated_shapes = [shape.get_rotation(center, -60*i) for i in range(6)]
#         for rotated_shape in rotated_shapes:
#             for row_i, row in enumerate(board):
#                 for col_i, _ in enumerate(row):
#                     if has_place(board, rotated_shape, row_i, col_i):
#                         place(board, rotated_shape, row_i, col_i)
#                         if solve(board, [s for s in shapes if s is not shape]):
#                             return True
#     return False
