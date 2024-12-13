from collections import Counter

from common.input import get_data, get_data_file

EXAMPLE = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def get_difference(data: list[list]) -> int:
    left = sorted(data[0])
    right = sorted(data[1])
    return sum(abs(a - b) for a, b in zip(left, right))


def get_frequency(data: list[list]) -> int:
    left = data[0]
    right = Counter(data[1])
    return sum(item * right.get(item, 0) for item in left)


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    data = get_data(source, True)
    return get_frequency(data) if part_b else get_difference(data)
