import re

from common.input import get_data_file
from days.day_13.day_13 import Machine, parse_machines

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


def solve_for_machine(machine: Machine) -> int:
    # a * a.x + b * b.x = p.x
    # a * a.y + b * b.y = p.y
    determinant = machine.a_x * machine.b_y - machine.b_x * machine.a_y

    if determinant == 0:
        return 0

    numerator_a = machine.prize_x * machine.b_y - machine.b_x * machine.prize_y
    numerator_b = machine.a_x * machine.prize_y - machine.prize_x * machine.a_y

    if numerator_a % determinant != 0:
        return 0
    if numerator_b % determinant != 0:
        return 0

    a = numerator_a // determinant
    b = numerator_b // determinant

    return TOKENS_A * a + TOKENS_B * b


def least_tokens_with_math(data: str, make_it_large: int) -> int:
    machines = parse_machines(data)
    least_tokens = 0
    for machine in machines:
        machine.prize_x += make_it_large
        machine.prize_y += make_it_large
        least_tokens += solve_for_machine(machine)
    return least_tokens


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    return least_tokens_with_math(source, 10000000000000 if part_b else 0)
