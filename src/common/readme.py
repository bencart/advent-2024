import os

from common.constants import CORRECT, WRONG


def get_readme_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", "..", "README.md")
    return os.path.normpath(relative_path)


def write_header():
    with open(get_readme_path(), "w", encoding="utf-8") as f:
        f.write(
            "\n".join(
                [
                    "# Advent of Code 2024",
                    "",
                    "https://adventofcode.com/2024/about",
                    "",
                    "## My Solutions:",
                    "",
                ]
            )
        )


def write_result(result: str):
    if CORRECT in result or WRONG in result:
        write_lines([result])
    else:
        write_lines([result.split("Result")[0]])


def write_lines(lines: list[str]):
    with open(get_readme_path(), "a", encoding="utf-8") as f:
        f.write("\n".join(lines + [""]))
