from collections import defaultdict
from itertools import combinations

from common.input import get_data_file, load_dict_grid

EXAMPLE = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def calculate_antinodes(
    coord: int, diff: int, n_opt: range, increasing: bool
) -> list[int]:
    if increasing:
        return [coord + (diff * n) for n in n_opt]
    return [coord - (diff * n) for n in n_opt]


def count_unique_antinodes(data: str, harmonics: bool):
    grid, rows, cols = load_dict_grid(data)
    antinodes = {}
    nodes = defaultdict(list)

    for cell, value in grid.items():
        if value != ".":
            nodes[value].append(cell)
    for frequency, cells in nodes.items():
        for (r1, c1), (r2, c2) in combinations(cells, 2):
            r_diff, c_diff = abs(r1 - r2), abs(c1 - c2)
            if harmonics:
                max_r = rows // r_diff + 1
                max_c = cols // c_diff + 1
                options = range(min(max_r, max_c))
            else:
                options = range(1, 2)

            antinodes_r1 = calculate_antinodes(r1, r_diff, options, r1 >= r2)
            antinodes_r2 = calculate_antinodes(r2, r_diff, options, r1 < r2)
            antinodes_c1 = calculate_antinodes(c1, c_diff, options, c1 >= c2)
            antinodes_c2 = calculate_antinodes(c2, c_diff, options, c1 < c2)

            for i in range(len(antinodes_r1)):
                x = antinodes_r1[i]
                y = antinodes_c1[i] if i < len(antinodes_c1) else -1
                if (x, y) in grid:
                    antinodes[(x, y)] = frequency
            for i in range(len(antinodes_r2)):
                x = antinodes_r2[i]
                y = antinodes_c2[i] if i < len(antinodes_c2) else -1
                if (x, y) in grid:
                    antinodes[(x, y)] = frequency
    return len(antinodes)


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    return count_unique_antinodes(source, harmonics=part_b)


if __name__ == "__main__":
    print(main(8, True, False))
