from pyqstars.core.piece import Piece


PIECES = {
    "blue": Piece("b", ((0, 0), (0, 1), (0, 2), (1, 1))),
    "green": Piece("g", ((0, 0), (0, 1), (1, 1), (2, 2))),
    "orange": Piece("o", ((0, 0), (0, 1), (1, 1))),
    "pink": Piece("p", ((0, 0), (0, 1), (1, 1), (2, 1))),
    "red": Piece("r", ((0, 0), (0, 1), (1, 0), (1, 1))),
    "violet": Piece("v", ((0, 0), (0, 1), (0, 2))),
    "yellow": Piece("y", ((0, 0), (0, 1), (0, 2), (1, 0)))
}


def inspect() -> None:
    separator = "\n\n# ---------------------------------------------- #\n\n"
    print(
        "\n",
        separator.join(
            f"{name}: {piece!r}\n\n{piece!s}"
            for name, piece in PIECES.items()
        ),
        "\n",
        sep=""
    )


def main() -> None:
    inspect()
    return None
