from dataclasses import dataclass


@dataclass(frozen=True)
class Piece:
    id: str
    tiles: tuple[tuple[int, int]]

    def get_matrix(self) -> list[list[bool]]:
        rows, cols = 4, 3
        matrix = [[False for _ in range(cols)] for _ in range(rows)]
        for row, col in self.tiles:
            matrix[row][col] = True
        return matrix

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
