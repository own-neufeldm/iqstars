from dataclasses import dataclass
from pprint import pprint
from typing import Self


@dataclass(frozen=True)
class Piece:
    CHAR_TO_TILE = {
        " ": False,
        "*": True
    }
    id: str
    color: str
    shape: list[list[bool]]

    @classmethod
    def from_string(cls, id: str, color: str, string: str) -> Self:
        conversion = [list(row) for row in string.split("\n")]
        shape: list[list[bool]] = []
        rows, cols = 7, 7
        for i in range(rows):
            row: list[bool] = []
            for j in range(cols):
                try:
                    char = conversion[i][j]
                except IndexError:
                    row.append(False)
                else:
                    row.append(cls.CHAR_TO_TILE[char])
            shape.append(row)
        return cls(id, color, shape)

    def dumps(self) -> str:
        tile_to_char = {v: k for k, v in type(self).CHAR_TO_TILE.items()}
        lines: list[str] = []
        for row in self.shape:
            line = [tile_to_char[tile] for tile in row]
            if string := "".join(line).rstrip():
                lines.append(string)
        return "\n".join(lines)

    def dump(self) -> None:
        return print(self.dumps())

    def inspect(self) -> str:
        pprint(self.shape)

    def __repr__(self) -> str:
        return self.dumps()

    def __str__(self) -> str:
        return self.inspect()


@dataclass(frozen=True)
class Board:
    FIELD_EMPTY = " "
    FIELD_UNAVAILABLE = "/"
    CHAR_TO_FIELD = {
        "-": FIELD_EMPTY,
        " ": FIELD_UNAVAILABLE
    }
    board: list[list[str]]

    @classmethod
    def from_string(cls, string: str) -> Self:
        conversion = [list(row) for row in string.split("\n")]
        board: list[list[str]] = []
        rows, cols = 7, 13
        for i in range(rows):
            if i % 2 == 1:
                board.append(list(cls.FIELD_UNAVAILABLE for _ in range(cols)))
                continue
            row: list[str] = []
            for j in range(cols):
                try:
                    char = conversion[i//2][j]
                except IndexError:
                    row.append(cls.FIELD_UNAVAILABLE)
                else:
                    try:
                        row.append(cls.CHAR_TO_FIELD[char])
                    except KeyError:
                        row.append(char)
            board.append(row)
        return cls(board)

    def dumps(self) -> str:
        field_to_char = {v: k for k, v in type(self).CHAR_TO_FIELD.items()}
        lines: list[str] = []
        for row in self.board:
            line: list[str] = []
            for field in row:
                try:
                    line.append(field_to_char[field])
                except KeyError:
                    line.append(field)
            if string := "".join(line).rstrip():
                lines.append(string)
        return "\n".join(lines)

    def dump(self) -> None:
        return print(self.dumps())

    def inspect(self) -> str:
        pprint(self.board)

    def __repr__(self) -> str:
        return self.dumps()

    def __str__(self) -> str:
        return self.inspect()

    # def solve(self, pieces: list[Piece]) -> bool:
    #     if not pieces:
    #         return True
    #     for piece in pieces:
    #         if Board.place(piece):
    #             Board.solve(board, pieces)
    #     return False
