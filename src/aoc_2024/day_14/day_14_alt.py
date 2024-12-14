from aoc_2024.day_14.day_14 import (
    EXAMPLE,
    safest_quadrant,
    parse_robots,
    visualise_robots,
)
from common.input import get_data_file


def find_tree(data: str, size: tuple[int, int]) -> int:
    robots = parse_robots(data, size)
    for i in range(1, size[0] ** 2 + size[1] ** 2):
        tracker = set()
        unique = True
        for robot in robots:
            robot.tick(i)
            if robot.location() in tracker:
                unique = False
                break
            tracker.add(robot.location())
        if unique:
            visualise_robots(robots, size)
            return i
        i += 1


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    size = (11, 7) if example else (101, 103)
    seconds = 100
    return find_tree(source, size) if part_b else safest_quadrant(source, size, seconds)
