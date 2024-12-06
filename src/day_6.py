import re

from common.input import get_data_file
from dayze.day6_part2 import main as part_b

EXAMPLE_1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

BLOCK = "#"
GUARD = ">"
VISIT = "O"
LEAVE_RE = re.compile(r"^(.*)(>[^#]*)$", re.MULTILINE)
BLOCK_RE = re.compile(r"^(.*)(>[^#]*)(#.*)$", re.MULTILINE)
DIRECTION_RE = re.compile(r"[\^v<>]", re.DOTALL)


def load_grid(data: str) -> str:
    lines = data.strip().split("\n")
    grid = "\n".join([line for line in lines if line.strip()])
    direction = DIRECTION_RE.search(data).group(0)
    grid = grid.replace(direction, GUARD)
    rotations = {"^": 3, "<": 2, "v": 1}
    for _ in range(rotations.get(direction, 0)):
        grid = rotate_grid(grid)
    return grid


def rotate_grid(grid: str) -> str:
    rows = grid.splitlines()
    columns = ["".join(row) for row in zip(*rows)]
    return "\n".join(columns[::-1])


def traverse_grid(data: str) -> str:
    grid = load_grid(data)
    while True:
        new_grid = LEAVE_RE.sub(movement, grid)
        if new_grid == grid:
            grid = BLOCK_RE.sub(movement, grid)
            grid = rotate_grid(grid)
        else:
            grid = new_grid
            break
    return grid


def visited_location_count(data: str) -> int:
    finished_map = traverse_grid(data)
    return finished_map.count(VISIT)


def movement(match: re.Match[str]) -> str:
    if match:
        before = match.group(1)
        move_path = match.group(2)
        blockage = match.group(3) if len(match.groups()) == 3 else ""
        visits = VISIT * (len(move_path) - 1)
        guard = GUARD if blockage else VISIT
        return f"{before}{visits}{guard}{blockage}"
    return match.group(0)


def main() -> None:
    example_a = EXAMPLE_1
    print(f"Day 6 Part A Example = {visited_location_count(example_a)}")
    part_a = get_data_file("day_6.txt")
    print(f"Day 6 Part A = {visited_location_count(part_a)}")

    part_b(EXAMPLE_1, "day_6.txt")
