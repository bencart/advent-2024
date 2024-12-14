import re

from common.input import get_data_file

EXAMPLE_1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
EXAMPLE_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

MUL_RE = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
DO_RE = re.compile(r"don't\(\).*?do\(\)", re.DOTALL)
DONT_RE = re.compile(r"don't\(\).*", re.DOTALL)


def get_multiples(data: str, filtered: bool = False) -> int:
    text = filter_donts(data) if filtered else data
    matches = MUL_RE.findall(text)
    return sum(int(a) * int(b) for a, b in matches)


def filter_donts(data: str) -> str:
    return DONT_RE.sub("", DO_RE.sub("", data))


def main(day: int, example: bool, part_b: bool) -> int:
    source = (
        EXAMPLE_2
        if example and part_b
        else EXAMPLE_1 if example else get_data_file(f"day_{day}.txt")
    )
    return get_multiples(source, filtered=part_b)
