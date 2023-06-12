from dataclasses import dataclass
from pprint import pprint
from typing import Iterable, Self


@dataclass(frozen=True)
class Piece:
    SHAPE_HEIGHT = 7
    SHAPE_WIDTH = 11
    id: str
    shape: list[list[bool]]

    @classmethod
    def from_tiles(cls, id: str, tiles: Iterable[tuple[int, int]]) -> Self:
        row_offset, col_offset = cls.SHAPE_HEIGHT // 2, cls.SHAPE_WIDTH // 2
        shape = [
            [False for _ in range(cls.SHAPE_WIDTH)]
            for _ in range(cls.SHAPE_HEIGHT)
        ]
        for row, col in tiles:
            shape[row+row_offset][col+col_offset] = True
        return cls(id, shape)

    def dumps(self) -> str:
        lines: list[str] = []
        for row in self.shape:
            line = ["X" if tile else "-" for tile in row]
            lines.append("".join(line))
        return "\n".join(lines)

    def dump(self) -> None:
        return print(self.dumps())

    def inspect(self) -> str:
        pprint(self.shape)

    def __repr__(self) -> str:
        return self.dumps()

    def __str__(self) -> str:
        return self.inspect()

    def _rotated(self, rotation: int) -> Self:
        if rotation == 0:
            return self
        ...

    def rotated(self, rotation: int) -> Self:
        if not 0 <= rotation <= 5:
            raise ValueError(
                f"Rotation must be between 0 and 5, inclusive. "
                f"Is {rotation}."
            )
        return self._rotated(rotation)

    def itertiles(self) -> Iterable[tuple[int, int]]:
        row_offset, col_offset = self.SHAPE_HEIGHT // 2, self.SHAPE_WIDTH // 2
        tiles: list[tuple[int, int]] = []
        for row_index, row in enumerate(self.shape):
            for col_index, tile in enumerate(row):
                if tile:
                    tiles.append((row_index-row_offset, col_index-col_offset))
        return tiles
