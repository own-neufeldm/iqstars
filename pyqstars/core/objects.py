from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Piece:
    id: str
    color: str


@dataclass(frozen=True)
class Board:
    board: list[list[str]]

    @classmethod
    def from_string(cls, string: str) -> Self:
        return cls([row.split(" ") for row in string.split("\n")])

    def solve(self, pieces: list[Piece]) -> bool:
        if not pieces:
            return True
        for piece in pieces:
            if Board.place(piece):
                Board.solve(board, pieces)
        return False

    def __str__(self) -> str:
        lines: list[str] = []
        for row in self.board:
            line: list[str] = []
            for char in row:
                line.append(char)
            lines.append(" ".join(line))
        return "\n".join(lines)
