from dataclasses import dataclass

from pyqstars.core.hex import Hex as Tile


@dataclass(frozen=True)
class Shape:
    id: str
    tiles: tuple[Tile]

    def get_matrix(self) -> list[list[bool]]:
        rows, cols = 7, 7
        matrix = [[False for _ in range(cols)] for _ in range(rows)]
        for hex in self.tiles:
            matrix[hex.row][hex.col] = True
        return matrix

    def rotate(self, center: Tile) -> None:
        for tile in self.tiles:
            tile.rotate(center)
        return None

    def __str__(self) -> str:
        unoccupied, occupied = "-", "*"
        lines: list[str] = []
        for row_i, row in enumerate(self.get_matrix()):
            line: list[str] = []
            for col in row:
                line.append(occupied if col else unoccupied)
            string = " ".join(line)
            if row_i % 2 == 1:
                string = " " + string
            lines.append(string)
        return "\n".join(lines)
