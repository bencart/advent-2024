import re
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from math import prod

from common.input import get_data_file

EXAMPLE = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

MIDDLE = (-1, -1)

ROBOT_PATTERN = r"p=([^,]*),([^\s]*) v=([^,]*),([^\s\n]*)"
ROBOT_RE = re.compile(ROBOT_PATTERN, re.DOTALL)


@dataclass
class Robot:
    p_x: int
    p_y: int
    v_x: int
    v_y: int
    grid_size: tuple[int, int]
    c_x: int = 0
    c_y: int = 0
    ticks: int = 0

    def __post_init__(self):
        self.c_x = self.p_x
        self.c_y = self.p_y

    def tick(self, total_ticks: int):
        size = self.grid_size
        count = total_ticks - self.ticks
        self.c_x = (self.c_x + (count * self.v_x)) % size[0]
        self.c_y = (self.c_y + (count * self.v_y)) % size[1]
        self.ticks = total_ticks

    def location(self) -> tuple[int, int]:
        return self.c_x, self.c_y

    def quadrant(self) -> tuple[int, int]:
        return quadrant_no_middle(self.location(), self.grid_size)

    def ninth(self) -> tuple[int, int]:
        return sub_area(self.location(), self.grid_size, 3)


@lru_cache(maxsize=None, typed=True)
def quadrant_no_middle(
    position: tuple[int, int], size: tuple[int, int]
) -> tuple[int, int]:
    x, y = position
    w, h = size
    mw, mh = w // 2, h // 2
    if x == mw or y == mh:
        return MIDDLE
    qx = 0 if x < mw else 1
    qy = 0 if y < mh else 1
    return qx, qy


@lru_cache(maxsize=None, typed=True)
def sub_area(
    position: tuple[int, int], size: tuple[int, int], divisions: int
) -> tuple[int, int]:
    x, y = position
    w, h = size
    mw, mh = w / divisions, h / divisions
    return min(divisions - 1, x // mw), min(divisions - 1, y // mh)


def parse_robots(data: str, size: tuple[int, int]) -> list[Robot]:
    robots = []
    for match in ROBOT_RE.finditer(data):
        robots.append(
            Robot(
                p_x=int(match.group(1)),
                p_y=int(match.group(2)),
                v_x=int(match.group(3)),
                v_y=int(match.group(4)),
                grid_size=size,
            )
        )
    return robots


def safest_quadrant(data: str, size: tuple[int, int], ticks: int) -> int:
    robots = parse_robots(data, size)
    quadrants = defaultdict(int)
    for robot in robots:
        robot.tick(ticks)
        quadrants[robot.quadrant()] += 1
    return prod([v for k, v in quadrants.items() if k != MIDDLE])


def visualise_robots(robots: list[Robot], size: tuple[int, int]):
    grid = {}

    for robot in robots:
        grid[robot.location()] = "*"

    for i in range(size[0]):
        line = ""
        for j in range(size[1]):
            line += grid.get((j, i), " ")
        print(line)


def get_ninths(robots: list[Robot]) -> (int, int, int, int):
    ninths = defaultdict(int)
    for robot in robots:
        ninths[robot.ninth()] += 1
    return {k: v for k, v in ninths.items() if k != MIDDLE}


def calculate_chi_square(ninths: dict[tuple[int, int], int]) -> float:
    robots = sum(ninths.values())
    observed = list(ninths.values())
    expected_count = robots / len(observed)
    chi_square = sum((o - expected_count) ** 2 / expected_count for o in observed)
    return chi_square


def find_tree(data: str, size: tuple[int, int]):
    robots = parse_robots(data, size)

    ninth_freedom = 8
    ninth_crit = 110 * ninth_freedom**0.5

    for i in range(1, size[0] ** 2 + size[1] ** 2):
        for robot in robots:
            robot.tick(i)

        ninths = get_ninths(robots)
        calculate_chi_square(ninths)
        chi_ninth = calculate_chi_square(ninths)

        if chi_ninth > ninth_crit:
            return i


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    size = (11, 7) if example else (101, 103)
    return find_tree(source, size) if part_b else safest_quadrant(source, size, 100)
