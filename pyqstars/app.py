from typing import Iterable

from pyqstars.core.shapes import Shape, Tile

SHAPES = {
    "blue": Shape("b", (Tile(3, 3), Tile(4, 3), Tile(5, 3), Tile(5, 4))),
    "violet": Shape("v", (Tile(3, 3), Tile(4, 3), Tile(5, 3)))
}


def inspect(shapes: Iterable[Shape]) -> None:
    separator = "\n\n# ---------------------------------------------- #\n\n"
    print(
        "\n",
        separator.join(f"{piece!r}\n\n{piece!s}" for piece in shapes),
        "\n",
        sep=""
    )


def main() -> None:
    center = Tile(3, 3)
    inspect(SHAPES["blue"].rotated(center, 60*i) for i in range(6))
