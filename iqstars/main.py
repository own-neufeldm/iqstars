import iqstars.app as app


def main() -> None:
    board = app.Board([
        ["-", "-", "-", "v", "v", "v", "o"],
        ["-", "-", "-", "-", "-", "o", "/"],
        ["p", "-", "p", "-", "-", "-", "o"],
        ["p", "p", "-", "-", "-", "-", "/"]
    ])
    pieces = [
        app.PIECES["blue"],
        app.PIECES["green"],
        app.PIECES["red"],
        app.PIECES["yellow"]
    ]
    app.solve(board, pieces)
    return None


if __name__ == "__main__":
    main()
