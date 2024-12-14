import re
from dataclasses import dataclass

from common.input import get_data_file

TOKENS_A = 3
TOKENS_B = 1

EXAMPLE = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

MACHINE_PATTERN = "A:.X([-+][0-9]*),.Y([-+][0-9]*)[^:]*:.X([-+][0-9]*),.Y([-+][0-9]*)[^:]*:.X=([0-9]*),.Y=([0-9]*)"
MACHINE_RE = re.compile(MACHINE_PATTERN, re.DOTALL)


@dataclass
class Machine:
    prize_x: int
    prize_y: int
    a_x: int
    a_y: int
    b_x: int
    b_y: int


def parse_machines(data: str) -> list[Machine]:
    machines = []
    for match in MACHINE_RE.finditer(data):
        machines.append(
            Machine(
                a_x=int(match.group(1)),
                a_y=int(match.group(2)),
                b_x=int(match.group(3)),
                b_y=int(match.group(4)),
                prize_x=int(match.group(5)),
                prize_y=int(match.group(6)),
            )
        )
    return machines


def find_combinations(target: int, a: int, b: int) -> set[tuple[int, int]]:
    combinations = set()
    for i in range(target // a + 1):
        remainder = target - i * a
        if remainder % b == 0:
            j = remainder // b
            combinations.add((i, j))
    return combinations


def least_tokens(data: str) -> int:
    machines = parse_machines(data)
    least_tokens = 0
    for machine in machines:
        combinations_x = find_combinations(machine.prize_x, machine.a_x, machine.b_x)
        combinations_y = find_combinations(machine.prize_y, machine.a_y, machine.b_y)
        combinations = combinations_x & combinations_y
        least_tokens += (
            min([a * TOKENS_A + b * TOKENS_B for a, b in combinations])
            if combinations
            else 0
        )
    return least_tokens


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    return least_tokens(source)
