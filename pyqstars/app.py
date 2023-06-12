from pyqstars.core.piece import Piece


def main() -> None:
    green_0 = Piece.from_tiles("g", [(0, 0), (0, 2), (1, 3), (2, 4)])
    print(green_0.itertiles())
    print()
    green_0.dump()
    print("\n# ---------------------------------------------- #\n")
    green_1 = Piece.from_tiles("g", [(0, 0), (1, 1), (2, 0), (3, -1)])
    print(green_1.itertiles())
    print()
    green_1.dump()
    print("\n# ---------------------------------------------- #\n")
    green_2 = Piece.from_tiles("g", [(0, 0), (1, -1), (1, -3), (1, -5)])
    print(green_2.itertiles())
    print()
    green_2.dump()
    print("\n# ---------------------------------------------- #\n")
    green_3 = Piece.from_tiles("g", [(0, 0), (0, -2), (-1, -3), (-2, -4)])
    print(green_3.itertiles())
    print()
    green_3.dump()
    print("\n# ---------------------------------------------- #\n")
    green_4 = Piece.from_tiles("g", [(0, 0), (-1, -1), (-2, 0), (-3, 1)])
    print(green_4.itertiles())
    print()
    green_4.dump()
    print("\n# ---------------------------------------------- #\n")
    green_5 = Piece.from_tiles("g", [(0, 0), (-1, 1), (-1, 3), (-1, 5)])
    print(green_5.itertiles())
    print()
    green_5.dump()
    return None


# PIECES = [
#     Piece("b", "blue"),
#     Piece("g", "green"),
#     Piece("o", "orange"),
#     Piece("p", "pink"),
#     Piece("r", "red"),
#     Piece("v", "violet"),
#     Piece("y", "yellow")
# ]


# def place(board: list[list[str]], piece: str) -> bool:
#     return True


# def solve(board: Board, pieces: list[Piece]) -> Board | None:
#     if not pieces:
#         return board
#     for piece in pieces:
#         if Board.place(piece):
#             Board.solve(board, pieces)
#     return None


# def get_unused_pieces(board: list[list[str]]) -> list[str]:
#     unused_pieces: list[str] = []
#     for piece in PIECES:
#         for rotattion in range(6):
#             rotated_piece: str = piece  # ... rotate somehow
#             if not any(rotated_piece in row for row in board):
#                 unused_pieces.append(rotated_piece)
#     return unused_pieces


# def main() -> None:
#     board = Board.from_string(textwrap.dedent("""\
#         v v v - - - -
#          - - - - - -
#         - - - - - - -
#          - - - - - -\
#     """))
#     print(
#         f"\nAttempting to solve:\n\n"
#         f"{board!s}\n\n"
#         f"# ---------------------------------------------- #\n",
#     )
#     if not Board.solve(PIECES.values()):
#         print("Board cannot be solved!\n")
#     else:
#         print(
#             f"Solution:\n\n"
#             f"{board!s}\n"
#         )
#     return None


# def main() -> None:
#     blue = Piece.from_string("b", "blue", textwrap.dedent("""\
#         * * *
#            *"""))
#     green = Piece.from_string("g", "green", textwrap.dedent("""\
#         * *
#            *
#             *"""))
#     orange = Piece.from_string("o", "orange", textwrap.dedent("""\
#         * *
#            *"""))
#     pink = Piece.from_string("p", "pink", textwrap.dedent("""\
#         * *
#            *
#           *"""))
#     red = Piece.from_string("r", "red", textwrap.dedent("""\
#         * *
#          * *"""))
#     violet = Piece.from_string("v", "violet", textwrap.dedent("""\
#         * * *"""))
#     yellow = Piece.from_string("y", "yellow", textwrap.dedent("""\
#         * * *
#          *"""))
#     board = Board.from_string(textwrap.dedent("""\
#         v v v r o y y
#          p p r r o y
#         p b p r o y g
#          b b b g g g"""))
#     board.inspect()
#     print("\n# ---------------------------------------------- #\n")
#     board.dump()
#     print("\n# ---------------------------------------------- #\n")
#     pink.inspect()
#     print("\n# ---------------------------------------------- #\n")
#     pink.dump()
