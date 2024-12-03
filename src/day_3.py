from common.input import get_data_file
import re


EXAMPLE_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

MUL_RE = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
DO_RE = re.compile(r"don't\(\).*?do\(\)", re.DOTALL)
DONT_RE = re.compile(r"don't\(\).*", re.DOTALL)


def get_multiples(data: str, filtered: bool = False) -> int:
    input = filter_donts(data) if filtered else data
    matches = MUL_RE.findall(input)
    return sum(int(a) * int(b) for a, b in matches)


def filter_donts(data: str) -> str:
    return DONT_RE.sub("", DO_RE.sub("", data))


def main() -> None:
    example_a = EXAMPLE_1
    print(f"Day 3 Part A Example = {get_multiples(example_a)}")
    part_a = get_data_file("day_3.txt")
    print(f"Day 3 Part A = {get_multiples(part_a)}")

    example_b = EXAMPLE_2
    print(f"Day 3 Part B Example = {get_multiples(example_b, filtered=True)}")
    part_b = get_data_file("day_3.txt")
    print(f"Day 3 Part B = {get_multiples(part_b, filtered=True)}")
