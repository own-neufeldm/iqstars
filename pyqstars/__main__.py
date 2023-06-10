import logging

import pyqstars.app


def configure_logging(level: int) -> None:
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")
    return None 


def main() -> None:
    configure_logging(logging.DEBUG)
    pyqstars.app.main()
    return None


if __name__ == "__main__":
    main()
