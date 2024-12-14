from common.input import get_data_file

EXAMPLE = "125 17"


def digits(i: int) -> int:
    return len(str(abs(i)))


def blink(stones: list[str]) -> list[str]:
    result = []
    for stone in stones:
        if stone == "0":
            result.append("1")
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            result.append(stone[:mid])
            result.append(str(int(stone[mid:])))
        else:
            result.append(str(int(stone) * 2024))
    return result


def count_stones(data: str, blinks: int) -> int:
    stones = [x for x in data.split()]
    for _ in range(blinks):
        stones = blink(stones)
    return len(stones)


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    blinks = 75 if part_b else 25
    return count_stones(source, blinks)
