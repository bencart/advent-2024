import re
from dataclasses import dataclass, field
from queue import Queue
from typing import Callable

from common.input import get_data_file

EXAMPLE_1 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

EXAMPLE_2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

INPUT_PATTERN = (
    r"Register A: ([0-9]+).*Register B: ([0-9]+).*Register C: ([0-9]+).*Program: (.*)"
)
INPUT_RE = re.compile(INPUT_PATTERN, re.DOTALL)


@dataclass
class ThreeBit(object):
    reg_a: int
    reg_b: int
    reg_c: int

    program: list[int]

    pointer: int = 0
    output: list = field(default_factory=list)
    command_map: list[Callable[[int], bool]] = field(default_factory=list)

    def __post_init__(self):
        self.command_map = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]

    def combo_operand(self, operand: int) -> int:
        if operand < 4:
            return operand
        if operand == 4:
            return self.reg_a
        if operand == 5:
            return self.reg_b
        if operand == 6:
            return self.reg_c
        raise

    def adv(self, operand: int):
        self.reg_a = self.reg_a >> self.combo_operand(operand)

    def bxl(self, operand: int):
        self.reg_b = self.reg_b ^ operand

    def bst(self, operand: int):
        self.reg_b = self.combo_operand(operand) % 8

    def jnz(self, operand: int):
        if self.reg_a != 0:
            self.pointer = operand
            return True

    def bxc(self, operand: int):
        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, operand: int):
        self.output.append(self.combo_operand(operand) % 8)

    def bdv(self, operand: int):
        self.reg_b = self.reg_a >> self.combo_operand(operand)

    def cdv(self, operand: int):
        self.reg_c = self.reg_a >> self.combo_operand(operand)

    def execute_program(self, validate: int = -1) -> str:
        while self.pointer < len(self.program):
            command = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            skip = self.command_map[command](operand)
            if not skip:
                self.pointer += 2
            if (
                validate >= 0
                and self.output
                and len(self.output) > validate
                and self.output[validate] != self.program[validate]
            ):
                break
        return ",".join(map(str, self.output))

    def reset(self):
        self.pointer = 0
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0
        self.output = []

    def reverse_engineer(self) -> int:
        length = len(self.program) - 1
        queue = Queue()
        queue.put((8**length, 8 ** (length + 1), length))
        while not queue.empty():
            lower, upper, index = queue.get()
            for guess in range(lower, upper, 8**index):
                self.reset()
                self.reg_a = guess
                self.execute_program(index)
                if self.output[index] == self.program[index]:
                    if index > 0:
                        queue.put((guess, guess + 8**index, index - 1))
                    else:
                        return guess
        return None


def parse_input(data: str) -> ThreeBit:
    match = INPUT_RE.search(data)
    return ThreeBit(
        reg_a=int(match.group(1)),
        reg_b=int(match.group(2)),
        reg_c=int(match.group(3)),
        program=[int(c.strip()) for c in match.group(4).strip().split(",")],
    )


def execute_program(data: str, reverse: bool) -> int:
    computer = parse_input(data)
    return computer.reverse_engineer() if reverse else computer.execute_program()


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    example_source = EXAMPLE_2 if part_b else EXAMPLE_1
    source = example_source if example else get_data_file(year, day)
    return execute_program(source, part_b)
