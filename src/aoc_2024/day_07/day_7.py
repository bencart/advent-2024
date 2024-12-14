import re

from common.input import get_data_file

EXAMPLE = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

INPUT_RE = re.compile("^([0-9]*): (.*)$")


def get_data(data: str) -> list[(int, list[int])]:
    lines = data.strip().split("\n")
    equations = []
    for line in lines:
        if not line.strip():
            continue
        match = INPUT_RE.match(line)
        target = int(match.group(1))
        subjects = [int(x.strip()) for x in match.group(2).split()]
        equations.append((target, subjects))
    return equations


def sum_possibles(data: str, concatenate: bool = False) -> int:
    equations = get_data(data)
    return sum(e[0] for e in equations if is_calcuable(e, concatenate=concatenate))


def is_calcuable(equation: tuple[int, list[int]], concatenate: bool = False) -> bool:
    total, parts = equation
    running_totals = [parts[0]]
    remaining_parts = parts[1:][::-1]

    while remaining_parts and running_totals:
        step = remaining_parts.pop()
        add_total = [rt + step for rt in running_totals]
        multiply_total = [rt * step for rt in running_totals]
        concatenate_total = []
        if concatenate:
            concatenate_total = [int(f"{rt}{step}") for rt in running_totals]
        step_totals = set(add_total + multiply_total + concatenate_total)
        running_totals = [r for r in step_totals if r <= total]
    return total in running_totals


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    return sum_possibles(source, concatenate=part_b)
