from typing import Iterable

from pyqstars.core.shapes import Shape, Tile

SHAPES = {
    "blue": Shape("b", (Tile(0, 0), Tile(1, 0), Tile(2, 0), Tile(1, 1))),
    "green": Shape("g", (Tile(0, 0), Tile(1, 0), Tile(1, 1), Tile(2, 2))),
    "orange": Shape("o", (Tile(0, 0), Tile(1, 0), Tile(1, 1))),
    "pink": Shape("p", (Tile(0, 0), Tile(1, 0), Tile(1, 1), Tile(1, 2))),
    "red": Shape("r", (Tile(0, 0), Tile(1, 0), Tile(0, 1), Tile(1, 1))),
    "violet": Shape("v", (Tile(0, 0), Tile(1, 0), Tile(2, 0))),
    "yellow": Shape("y", (Tile(0, 0), Tile(1, 0), Tile(2, 0), Tile(0, 1)))
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
    center = Tile(0, 0)
    inspect(
        shape.get_rotation(center, -60*i)
        for shape in SHAPES.values()
        for i in range(6)
    )
    return None
