from typing import Iterable

from pyqstars.core.shape import Tile, Shape


SHAPES = {
    "blue": Shape("b", (Tile(3, 3), Tile(4, 3), Tile(5, 3), Tile(4, 4)))
}


def inspect(shapes: Iterable[Shape]) -> None:
    if shapes is None:
        shapes = SHAPES.values()
    separator = "\n\n# ---------------------------------------------- #\n\n"
    print(
        "\n",
        separator.join(f"{piece!r}\n\n{piece!s}" for piece in shapes),
        "\n",
        sep=""
    )


def inspect_rotation(shape: Shape) -> None:
    center = shape.tiles[0]
    print(shape)
    for _ in range(6):
        print()
        shape.rotate(center)
        print(shape)
    return None


def main() -> None:
    shape = SHAPES["blue"]
    inspect_rotation(shape)

