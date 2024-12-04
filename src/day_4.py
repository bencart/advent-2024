from common.input import get_data, get_data_file
import re

EXAMPLE_1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def find_occurrances(grid: str, target: str) -> int:
    reversed = target[::-1]
    search_strings = get_all_strings(grid)
    return sum(search.count(target) + search.count(reversed) for search in search_strings)


def get_all_strings(grid: str) -> list[str]:
    lines = [l for l in grid.splitlines() if l.strip()]
    num_rows = len(lines)
    num_cols = max(len(line) for line in lines)

    rows = lines
    columns = ["".join(line[col] for line in lines) for col in range(num_cols)]

    diagonals_tl_br = [
        "".join(lines[row][d - row] for row in range(num_rows) if 0 <= d - row < num_cols)
        for d in range(num_rows + num_cols - 1)
    ]
    diagonals_tr_bl = [
        "".join(
            lines[row][row + d - (num_rows - 1)] for row in range(num_rows) if 0 <= row + d - (num_rows - 1) < num_cols)
        for d in range(num_rows + num_cols - 1)
    ]
    return rows + columns + diagonals_tl_br + diagonals_tr_bl


END_PATTERNS = {
    "f_f": re.compile(r"(?=M.M)"),
    "f_b": re.compile(r"(?=M.S)"),
    "b_f": re.compile(r"(?=S.M)"),
    "b_b": re.compile(r"(?=S.S)"),
}
TOP_BOTTOM = {
    "f_f": "b_b",
    "b_b": "f_f"
}
MID_PATTERN = re.compile(r"(?=.A.)")


def find_cross_masses(grid: str) -> int:
    lines = [l for l in grid.splitlines() if l.strip()]
    count = 0
    for i in range(len(lines) - 2):
        checks = {
            ix:TOP_BOTTOM.get(name, name)
            for name, pattern in END_PATTERNS.items()
            for ix in get_indices(lines[i], pattern)
        }
        mid_ix = get_indices(lines[i+1], MID_PATTERN)
        for ix, name in checks.items():
            if ix in mid_ix and END_PATTERNS[name].match(lines[i+2][ix:ix+3]):
                count += 1
    return count


def get_indices(line: str, pattern: re.Pattern) -> list[int]:
    return [match.start() for match in pattern.finditer(line)]


def main() -> None:
    target = "XMAS"
    example_a = EXAMPLE_1
    print(f"Day 4 Part A Example = {find_occurrances(example_a, target)}")
    part_a = get_data_file("day_4.txt")
    print(f"Day 4 Part A = {find_occurrances(part_a, target)}")

    example_b = EXAMPLE_1
    print(f"Day 4 Part B Example = {find_cross_masses(example_b)}")
    part_b = get_data_file("day_4.txt")
    print(f"Day 4 Part B = {find_cross_masses(part_b)}")
