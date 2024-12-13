from collections import defaultdict
from itertools import combinations

from common.input import get_data_file, load_grid

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


def count_unique_antinodes(data: str, harmonics: bool = False) -> int:
    grid = load_grid(data)
    antinodes = [["." for _ in row] for row in grid]
    row_count = len(grid)
    col_count = len(grid[0])

    def in_grid(r: int, c: int) -> bool:
        return 0 <= r < row_count and 0 <= c < col_count

    nodes = defaultdict(list)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != ".":
                nodes[cell].append((r, c))
    for frequency, cells in nodes.items():
        for (r1, c1), (r2, c2) in combinations(cells, 2):
            r_diff, c_diff = abs(r1 - r2), abs(c1 - c2)

            if harmonics:
                max_r = int(row_count / r_diff) + 1
                max_c = int(col_count / c_diff) + 1
                options = range(min(max_r, max_c))
            else:
                options = range(1, 2)

            antinodes_r1 = calculate_antinodes(r1, r_diff, options, r1 >= r2)
            antinodes_r2 = calculate_antinodes(r2, r_diff, options, r1 < r2)
            antinodes_c1 = calculate_antinodes(c1, c_diff, options, c1 >= r2)
            antinodes_c2 = calculate_antinodes(c2, c_diff, options, r1 < r2)

            for i in range(len(antinodes_r1)):
                r1 = antinodes_r1[i]
                c1 = antinodes_c1[i] if i < len(antinodes_c1) else -1
                if in_grid(r1, c1):
                    antinodes[r1][c1] = "#"
            for i in range(len(antinodes_r2)):
                r2 = antinodes_r2[i]
                c2 = antinodes_c2[i] if i < len(antinodes_c2) else -1
                if in_grid(r2, c2):
                    antinodes[r2][c2] = "#"
    return sum(row.count("#") for row in antinodes)


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    return count_unique_antinodes(source, harmonics=part_b)
