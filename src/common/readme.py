import os

from common.constants import CORRECT, WRONG, YEAR


def get_readme_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", "..", "README.md")
    return os.path.normpath(relative_path)


def write_readme_header():
    with open(get_readme_path(), "w", encoding="utf-8") as f:
        f.write(
            "\n".join(
                [
                    f"# Advent of Code {YEAR}",
                    "",
                    f"https://adventofcode.com/{YEAR}/about",
                    "",
                    "",
                ]
            )
        )


def write_readme_solution_links(main_methods: dict[int, list]):
    lines = ["## My Solutions:", ""]

    for day in sorted(main_methods.keys()):
        day_methods = main_methods[day]
        main = [r for r in day_methods if not r.get("alternate") and r.get("main")][0]
        alt = [r for r in day_methods if r.get("alternate") and r.get("main")]
        lines.append(
            f"{day}. https://github.com/bencart/advent-2024/blob/main/src/aoc_{YEAR}/{main["path"]}.py"
        )
        if alt:
            for r in alt:
                lines.append(
                    f"    - https://github.com/bencart/advent-2024/blob/main/src/aoc_{YEAR}/{r["path"]}.py"
                )
    write_lines(lines + [""])


def write_readme_output_header():
    write_lines(["## My Output:", "", "```text"])


def write_readme_footer():
    write_lines(["```", "", ""])


def write_readme_result(result: str):
    if CORRECT in result or WRONG in result:
        write_lines([result])
    else:
        write_lines([result.split("Result")[0]])


def write_lines(lines: list[str]):
    with open(get_readme_path(), "a", encoding="utf-8") as f:
        f.write("\n".join(lines + [""]))
