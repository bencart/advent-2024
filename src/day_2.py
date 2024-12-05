from common.input import get_data, get_data_file

EXAMPLE_1 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

def are_diffs_safe(diffs: list[int]) -> bool:
    is_relative = all(1 <= abs(diff) <= 3 for diff in diffs)
    is_ascending = all(diff >= 0 for diff in diffs)
    is_descending = all(diff <= 0 for diff in diffs)
    return is_relative and (is_ascending or is_descending)


def is_safe(items: list[int], almost:bool = False) -> bool:
    num = len(items)
    diffs = [items[i + 1] - items[i] for i in range(num - 1)]
    if not almost:
        return are_diffs_safe(diffs)

    for i in range(num):
        if i == 0:
            subset = diffs[1:]
        elif i == num - 1:
            subset = diffs[:-1]
        else:
            subset = diffs[:i - 1] + [items[i + 1] - items[i - 1]] + diffs[i + 1:]
        if are_diffs_safe(subset):
            return True

    return False

def count_safe(rows: list[list[int]], almost: bool = False) -> int:
    return sum(1 for row in rows if is_safe(row, almost))


def main() -> None:
    example_a = get_data(EXAMPLE_1)
    print(f"Day 2 Part A Example = {count_safe(example_a)}")
    part_a = get_data(get_data_file("day_2.txt"))
    print(f"Day 2 Part A = {count_safe(part_a)}")

    example_b = get_data(EXAMPLE_1)
    print(f"Day 2 Part B Example = {count_safe(example_b, almost=True)}")
    part_b = get_data(get_data_file("day_2.txt"))
    print(f"Day 2 Part B = {count_safe(part_b, almost=True)}")
