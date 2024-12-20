import numpy as np

from aoc_2024.day_20.day_20 import EXAMPLE, sum_c, dif_c
from common.constants import ADJACENT
from common.input import get_data_file, load_dict_grid
from common.types import Grid


def build_path(grid: Grid) -> np.ndarray:
    start = next(coord for coord, value in grid.items() if value == "S")
    d = (0, 0)
    path = [start]
    c = start
    while grid.get(c) != "E":
        point = next(sum_c(c, dx) for dx in (ADJACENT - {d}) if grid.get(sum_c(c, dx), "#") != "#")
        d = dif_c(c, point)
        path.append(point)
        c = point
    return np.array(path)


def find_cheats(data: str, min_saving: int, max_cutting: int):
    grid, rows, cols = load_dict_grid(data)
    path = build_path(grid)
    cheats = 0
    nodes = len(path)

    for early in range(nodes - 1):
        deltas = np.abs(path[early + 1:] - path[early])
        manhattan_distances = deltas.sum(axis=1)

        valid_mask = manhattan_distances <= max_cutting
        valid_indices = np.where(valid_mask)[0]
        valid_distances = manhattan_distances[valid_mask]
        path_distances = valid_indices + 1
        savings = path_distances - valid_distances

        cheats += np.sum(savings >= min_saving)
    return cheats


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    min_saving = 100 if not example else 50 if part_b else 1
    max_cutting = 20 if part_b else 2
    return find_cheats(source, min_saving, max_cutting)
