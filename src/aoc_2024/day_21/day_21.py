from dataclasses import dataclass, field
from typing import Optional

from common.input import get_data_file, get_lines
from common.types import Coordinate, Grid

EXAMPLE = """
029A
980A
179A
456A
379A
"""

NUMERIC_KEYPAD = {
    (0, 0): "7", (1, 0): "8", (2, 0): "9",
    (0, 1): "4", (1, 1): "5", (2, 1): "6",
    (0, 2): "1", (1, 2): "2", (2, 2): "3",
    (1, 3): "0", (2, 3): "A",
}

ARROW_KEYPAD = {
    (1, 0): "^", (2, 0): "A",
    (0, 1): "<", (1, 1): "v", (2, 1): ">",
}

DIRECTIONS = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}
MOVES = {v: k for k, v in DIRECTIONS.items()}


def sum_c(a: Coordinate, b: Coordinate) -> Coordinate:
    return (a[0] + b[0], a[1] + b[1])


def dif_c(a: Coordinate, b: Coordinate) -> Coordinate:
    return (a[0] - b[0], a[1] - b[1])


def get_moves(from_co: Coordinate, to_co: Coordinate) -> list[Coordinate]:
    moves = []
    dx, dy = dif_c(to_co, from_co)
    for direction in DIRECTIONS:
        d_dx, d_dy = DIRECTIONS[direction]
        if d_dx != 0 and dx // d_dx > 0:
            moves += [(d_dx, d_dy)] * (dx // d_dx)
        elif d_dy != 0 and dy // d_dy > 0:
            moves += [(d_dx, d_dy)] * (dy // d_dy)
    return moves


def all_buttons(from_co: Coordinate, moves: list[Coordinate]) -> list[Coordinate]:
    result = [from_co]
    current = from_co
    for move in moves:
        current = sum_c(current, move)
        result.append(current)
    return result


@dataclass
class Layout():
    layout: Grid
    _path_options: dict[tuple[str, str], list[str]] = field(default_factory=dict)

    def __post_init__(self):
        for from_co, from_v in self.layout.items():
            for to_co, to_v in self.layout.items():
                moves = get_moves(from_co, to_co)
                path_a, valid_a = self._get_path(from_co, moves)
                path_b, valid_b = self._get_path(from_co, moves[::-1])

                path_a = path_a if valid_a else path_b
                path_b = path_b if valid_b else path_a

                self._path_options[(from_v, to_v)] = [path_a, path_b]

    def _get_path(self, from_co: Coordinate, moves: list[Coordinate]) -> tuple[str, bool]:
        buttons = all_buttons(from_co, moves)
        valid = all(co in self.layout.keys() for co in buttons)
        return "".join([MOVES.get(m) for m in moves] + ["A"]), valid

    def items(self):
        return self.layout.items()

    def path_options(self, key: tuple[str, str]) -> list[str]:
        return self._path_options.get(key, [])


@dataclass
class Keypad():
    layout: Layout
    child: Optional["Keypad"] = None
    _route_dict: dict[tuple, str] = field(default_factory=dict)

    def __post_init__(self):
        self.pointer = next(k for k, v in self.layout.items() if v == "A")
        self._populate_routes()

    def _populate_routes(self):
        for from_co, from_v in self.layout.items():
            for to_co, to_v in self.layout.items():
                paths = self.layout.path_options((from_v, to_v))
                if self.child is None:
                    self._route_dict[(from_v, to_v)] = paths[0]
                else:
                    a = paths[0]
                    a_path = self.child.shortest_path(a)
                    b = paths[-1]
                    b_path = self.child.shortest_path(b) if a != b else a_path
                    self._route_dict[(from_v, to_v)] = b_path if len(b_path) < len(a_path) else a_path

    def shortest_path(self, path: str):
        movements = "A" + path
        result = ""
        for i in range(len(movements) - 1):
            from_m = movements[i]
            to_m = movements[i + 1]
            result += self._route_dict[(from_m, to_m)]
        return result


def enter_keypad(data: str, arrows: int):
    arrow_keys = Layout(ARROW_KEYPAD)
    number_keys = Layout(NUMERIC_KEYPAD)
    data_entry = Keypad(arrow_keys)
    child = data_entry
    for i in range(arrows - 1):
        child = Keypad(arrow_keys, child)
    numeric = Keypad(number_keys, child)
    codes = get_lines(data)
    complexities = []
    for code in codes:
        keys = numeric.shortest_path(code)
        complexities.append(int(code[:3]) * len(keys))
    return sum(complexities)


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    arrows = 25 if part_b else 2
    return enter_keypad(source, arrows)
