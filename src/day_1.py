from common.input import get_data, get_data_file
from collections import Counter


EXAMPLE_1 = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

EXAMPLE_2 = """
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
    assert len(left) == len(right), "Both lists must have the same length"
    return sum(abs(a - b) for a, b in zip(left, right))


def get_frequency(data: list[list]) -> int:
    left = data[0]
    right = Counter(data[1])
    return sum(item * right.get(item, 0) for item in left)


def main() -> None:
    example_a = get_data(EXAMPLE_1, True)
    print(f"Day 1 Part A Example = {get_difference(example_a)}")
    part_a = get_data(get_data_file("day_1.txt"), True)
    print(f"Day 1 Part A = {get_difference(part_a)}")

    example_b = get_data(EXAMPLE_2, True)
    print(f"Day 1 Part B Example = {get_frequency(example_b)}")
    part_b = get_data(get_data_file("day_1.txt"), True)
    print(f"Day 1 Part B = {get_frequency(part_b)}")
