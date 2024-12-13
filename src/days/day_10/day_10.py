from common.constants import ADJACENT
from common.input import get_data_file, load_grid

EXAMPLE = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def calculate_trailhead_ends(
    grid: list[list[int]], rows: int, cols: int, indexer: dict[int, set]
) -> int:
    end_grid = [[set() for _ in range(cols)] for _ in range(rows)]
    for r, c in indexer[9]:
        end_grid[r][c].add((r, c))

    for val in range(8, -1, -1):
        for r, c in indexer[val]:
            ends = set()
            for dr, dc in ADJACENT:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == val + 1:
                    ends.update(end_grid[nr][nc])
            end_grid[r][c] = ends
    return sum(len(end_grid[r][c]) for (r, c) in indexer[0])


def calculate_trailhead_rating(
    grid: list[list[int]], rows: int, cols: int, indexer: dict[int, set]
):
    count_grid = [[0] * cols for _ in range(rows)]
    for r, c in indexer[9]:
        count_grid[r][c] = 1

    for val in range(8, -1, -1):
        for r, c in indexer[val]:
            total_count = 0
            for dr, dc in ADJACENT:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == val + 1:
                    total_count += count_grid[nr][nc]
            count_grid[r][c] = total_count

    return sum(count_grid[r][c] for (r, c) in indexer[0])


def calculate_trailhead_scores(data: str, rating: bool = False) -> int:
    grid = load_grid(data)
    grid = [[int(c) for c in row] for row in grid]
    rows, cols = len(grid), len(grid[0])

    indexer = {i: set() for i in range(10)}
    for r in range(rows):
        for c in range(cols):
            indexer[grid[r][c]].add((r, c))

    return (
        calculate_trailhead_rating(grid, rows, cols, indexer)
        if rating
        else calculate_trailhead_ends(grid, rows, cols, indexer)
    )


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    return calculate_trailhead_scores(source, part_b)
