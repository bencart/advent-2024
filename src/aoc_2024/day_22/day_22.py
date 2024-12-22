from collections import deque, defaultdict

from common.input import get_data_file, get_lines

MAX_ITERATIONS = 2000

EXAMPLE_1 = """
1
10
100
2024
"""

EXAMPLE_2 = """
1
2
3
2024
"""


def mix(secret_number: int, mixture: int) -> int:
    return mixture ^ secret_number


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def calculate_secret_number(secret_number: int) -> int:
    secret_number = prune(mix(secret_number, secret_number * 64))
    secret_number = prune(mix(secret_number, secret_number // 32))
    return prune(mix(secret_number, secret_number * 2048))


def calculate_secret_numbers(data: str):
    starting_numbers = [int(i) for i in get_lines(data)]
    secret_numbers = []
    for starting_number in starting_numbers:
        secret_number = starting_number
        for i in range(MAX_ITERATIONS):
            secret_number = calculate_secret_number(secret_number)
        secret_numbers.append(secret_number)
    return sum(secret_numbers)


def instruct_monkey(data: str) -> int:
    starting_numbers = [int(i) for i in get_lines(data)]
    sequences = defaultdict(int)
    for i, starting_number in enumerate(starting_numbers):
        queue = deque(maxlen=4)
        seen = set()
        secret_number = starting_number
        for _ in range(MAX_ITERATIONS):
            next_number = calculate_secret_number(secret_number)
            prev_digit = secret_number % 10
            next_digit = next_number % 10
            curr_diff = next_digit - prev_digit
            queue.append(curr_diff)
            if len(queue) == 4:
                key = tuple(queue)
                if key not in seen:
                    sequences[key] += next_digit
                    seen.add(key)
            secret_number = next_number
    return max(sequences.values())


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE_2 if example and part_b else EXAMPLE_1 if example else get_data_file(year, day)
    return instruct_monkey(source) if part_b else calculate_secret_numbers(source)
