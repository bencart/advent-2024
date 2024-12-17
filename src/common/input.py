import os

import requests

from common.constants import URL_TEMPLATE, COOKIE


def get_data_file_path(file_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", "..", "data", file_name)
    return os.path.normpath(relative_path)


def get_data_file(year: int, day: int) -> str:
    path = get_data_file_path(f"{year}-{day}.txt")
    if not os.path.exists(path):
        url = URL_TEMPLATE.format(year=year, day=day)
        with requests.get(
                url, headers={"Cookie": f"session={COOKIE}"}, stream=True
        ) as r:
            with open(path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def get_lines(
        data: str, strip_empty: bool = True, strip_lines: bool = True
) -> list[str]:
    lines = data.strip().split("\n")
    if strip_empty:
        lines = [line for line in lines if line and line.strip()]
    if strip_lines:
        lines = [line.strip() for line in lines]
    return lines


def get_data(data: str, column: bool = False):
    lines = data.strip().split("\n")
    rows = [list(map(int, line.split())) for line in lines]
    if not column:
        return rows
    columns = list(zip(*rows))
    return [list(col) for col in columns]


def load_grid(data: str) -> list[list[str]]:
    lines = data.strip().splitlines()
    return [list(line) for line in lines if line.strip()]


def load_dict_grid(data: str) -> (dict[str], int, int):
    grid = load_grid(data)
    return (
        {(r, c): grid[r][c] for r in range(len(grid)) for c in range(len(grid[0]))},
        len(grid),
        len(grid[0]),
    )
