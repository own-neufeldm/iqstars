import logging
import sys
from pathlib import Path


ROOT_DIR = Path(sys.argv[0]).joinpath("../..").resolve()
SRC_DIR = ROOT_DIR / "project_name"
PYPROJECT_FILE = ROOT_DIR / "pyproject.toml"
README_FILE = ROOT_DIR / "README.md"


def get_project_name() -> str:
    value: str
    prompt = "Please provide a package name: "
    while True:
        value = input(prompt).strip()
        if value:
            break
        print("You have to specify a value ...")
    return value


def get_project_description() -> str:
    value: str
    prompt = "Please provide a package description: "
    while True:
        value = input(prompt).strip()
        if value:
            break
        print("You have to specify a value ...")
    return value


def get_project_classifier_operating_system() -> str:
    value: str
    help_url = "https://pypi.org/classifiers/"
    default = "OS Independent"
    prompt = (
        f"Please provide an operating system classifier ...\n"
        f"  See here for a list of possible values: {help_url}\n"
        f"  Leave empty for default value: {default}\n"
        f": "
    )
    value = input(prompt).strip()
    if not value:
        value = default
    return value


def get_project_requires_python() -> str:
    value: str
    default = ">=" + ".".join(str(e) for e in sys.version_info[:2])
    prompt = (
        f"Please provide a Python version requirement ...\n"
        f"  Leave empty for default value: {default}\n"
        f": "
    )
    value = input(prompt).strip()
    if not value:
        value = default
    return value


def setup_package() -> None:
    substitutions = {
        "PROJECT_NAME": get_project_name(),
        "PROJECT_DESCRIPTION": get_project_description(),
        "PROJECT_REQUIRES_PYTHON": get_project_requires_python(),
        "PROJECT_CLASSIFIER_OPERATING_SYSTEM":
        get_project_classifier_operating_system()
    }
    replace_all_in_file(PYPROJECT_FILE, substitutions)
    replace_all_in_file(README_FILE, substitutions)
    format_src(SRC_DIR, substitutions["PROJECT_NAME"])
    return None


def replace_all_in_file(file: Path, substitutions: dict[str, str]) -> None:
    lines = []
    with open(file) as f:
        for line in f:
            for old, new in substitutions.items():
                line = line.replace(f"${{{old}}}", new)
            lines.append(line)
    with open(file, "w") as f:
        for line in lines:
            f.write(line)


def format_src(src_dir: Path, name: str) -> None:
    src_dir.rename(name)
    return None


def configure_logging() -> None:
    logging.basicConfig(format="[%(levelname)s] %(message)s")
    return None


def main() -> None:
    configure_logging()
    setup_package()
    return None


if __name__ == "__main__":
    main()
