import textwrap


def solve(board: list[list[str]]) -> list[list[str]]:
    return board


def dumps(board: list[list[str]]) -> str:
    lines: list[str] = []
    for row in board:
        line = []
        for char in row:
            line.append(char.upper())
        lines.append(" ".join(line))
    return "\n".join(lines)


def main() -> None:
    board = textwrap.dedent("""\
        v v v - - - -
         - - - - - -
        - - - - - - -
         - - - - - -\
    """)
    board = [row.split(" ") for row in board.split("\n")]
    solution = solve(board)
    print(
        "",
        "Attempting to solve:\n",
        dumps(board),
        "\n# ---------------------------------------------- #\n",
        "Solution:\n",
        dumps(solution),
        "",
        sep="\n"
    )
    return None
