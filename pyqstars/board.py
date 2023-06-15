from pyqstars.shapes import Shape


FIELD_EMPTY = " "
FIELD_UNAVAILABLE = "/"
CHAR_TO_FIELD = {
    "-": FIELD_EMPTY,
    " ": FIELD_UNAVAILABLE
}


def from_string(string: str) -> list[list[str]]:
    ...


def dump(board: list[list[str]]) -> None:
    field_to_char = {v: k for k, v in CHAR_TO_FIELD.items()}
    lines: list[str] = []
    for row in board:
        line: list[str] = []
        for field in row:
            try:
                line.append(field_to_char[field])
            except KeyError:
                line.append(field)
        if string := "".join(line).rstrip():
            lines.append(string)
    print("\n".join(lines))


def can_tile_be_placed_at(board: list[list[str]], row: int, col: int) -> bool:
    return board[row][col] == FIELD_EMPTY


def place_tile_at(board: list[list[str]], tile: str, row: int, col: int) -> bool:
    if not can_tile_be_placed_at(board, row, col):
        return False
    board[row][col] = tile
    return True


def place_piece_at(board: list[list[str]], piece: Shape, row: int, col: int) -> bool:
    for tile_row, tile_col in piece.itertiles():
        if not place_tile_at(board, piece.id, tile_row+row, tile_col+col):
            return False
    return True


def place_piece(board: list[list[str]], piece: Shape) -> bool:
    for rotation in range(6):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if place_piece_at(board, piece.get_rotation(rotation), row, col):
                    return True
    return False


def solve(board: list[list[str]], pieces: list[Shape]) -> bool:
    if not pieces:
        dump(board)
        return True
    for piece in pieces:
        if place_piece(board, piece):
            pieces.remove(piece)
            solve(board, pieces)
    return False
