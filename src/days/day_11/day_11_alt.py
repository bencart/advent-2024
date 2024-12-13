from collections import defaultdict

from common.input import get_data_file
from days.day_11.day_11 import EXAMPLE


def blink_fast(stones: dict[int, int]) -> dict[int, int]:
    result = defaultdict(int)
    for value, count in stones.items():
        value_str = str(value)
        if value == 0:
            result[1] += count
        elif len(value_str) % 2 == 0:
            mid = len(value_str) // 2
            left = int(value_str[:mid])
            right = int(value_str[mid:])
            result[left] += count
            result[right] += count
        else:
            new_value = value * 2024
            result[new_value] += count
    return result


def count_stones_fast(data: str, blinks: int) -> int:
    stones = defaultdict(int)
    for stone in data.split():
        stones[int(stone)] += 1

    for _ in range(blinks):
        stones = blink_fast(stones)

    return sum(stones.values())


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    blinks = 75 if part_b else 25
    return count_stones_fast(source, blinks)
