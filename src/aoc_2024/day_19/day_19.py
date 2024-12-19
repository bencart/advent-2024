from collections import defaultdict

from common.input import get_data_file, get_lines

EXAMPLE = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def parse_input(data: str) -> tuple[set[str], list[str]]:
    lines = get_lines(data)
    available = {p.strip() for p in lines[0].split(",")}
    patterns = [lines[i] for i in range(1, len(lines))]
    return available, patterns


def is_solvable(pattern: str, available: set[str]) -> bool:
    length = len(pattern)
    solvable = [False] * (length + 1)
    solvable[0] = True

    for i in range(1, length + 1):
        for j in range(i):
            if solvable[j] and pattern[j:i] in available:
                solvable[i] = True
                break
    return solvable[length]


def find_solvable_patterns(patterns: list[str], available: set[str]) -> list[str]:
    solvable_patterns = []
    for pattern in patterns:
        if is_solvable(pattern, available):
            solvable_patterns.append(pattern)
    return solvable_patterns


def count_solutions(pattern: str, available: set[str]) -> int:
    length = len(pattern)
    lengths = defaultdict(list)
    for a in available:
        lengths[len(a)].append(a)
    solutions = [0] * (length + 1)
    solutions[0] = 1

    for i in range(1, length + 1):
        for a_length, a_patterns in lengths.items():
            if i >= a_length:
                subst = pattern[i - a_length: i]
                if subst in a_patterns:
                    solutions[i] += solutions[i - a_length]
    return solutions[length]


def count_all_possible_solutions(patterns: list[str], available: set[str]) -> int:
    all_solutions = 0
    for pattern in patterns:
        answer = count_solutions(pattern, available)
        all_solutions += answer
    return all_solutions


def find_towels(data: str, all_possibles: bool) -> int:
    available, patterns = parse_input(data)
    solvable_patterns = find_solvable_patterns(patterns, available)
    if all_possibles:
        return count_all_possible_solutions(solvable_patterns, available)
    return len(solvable_patterns)


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    return find_towels(source, part_b)
