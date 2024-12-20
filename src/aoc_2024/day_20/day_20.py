from common.constants import ADJACENT
from common.input import get_data_file, load_dict_grid
from common.types import Coordinate, Grid

EXAMPLE = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def build_path(grid: Grid) -> list[Coordinate]:
    start = next(coord for coord, value in grid.items() if value == "S")
    d = (0, 0)
    path = [start]
    c = start
    while grid.get(c) != "E":
        point = next(sum_c(c, dx) for dx in (ADJACENT - {d}) if grid.get(sum_c(c, dx), "#") != "#")
        d = dif_c(c, point)
        path.append(point)
        c = point
    return path


def sum_c(a: Coordinate, b: Coordinate) -> Coordinate:
    return (a[0] + b[0], a[1] + b[1])


def dif_c(a: Coordinate, b: Coordinate) -> Coordinate:
    return (a[0] - b[0], a[1] - b[1])


def manhattan(a: Coordinate, b: Coordinate) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_cheats(data: str, min_saving: int, max_cutting: int):
    grid, rows, cols = load_dict_grid(data)
    path = build_path(grid)

    cheats = 0

    for early in range(len(path) - 1):
        for late in range(early + min_saving + 1, len(path)):
            cheat_distance = manhattan(path[early], path[late])
            if cheat_distance > max_cutting:
                continue
            path_distance = late - early
            saving = path_distance - cheat_distance
            if saving >= min_saving:
                cheats += 1
    return cheats


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    min_saving = 100 if not example else 50 if part_b else 1
    max_cutting = 20 if part_b else 2
    return find_cheats(source, min_saving, max_cutting)
