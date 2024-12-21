from dataclasses import dataclass, field

from aoc_2024.day_21.day_21 import EXAMPLE, NUMERIC_KEYPAD, ARROW_KEYPAD, Layout, Keypad as KP
from common.input import get_data_file, get_lines


@dataclass
class Keypad(KP):
    _route_dict: dict[tuple, int] = field(default_factory=dict)

    def _populate_routes(self):
        for key, value in self.layout.items():
            for n_key, n_value in self.layout.items():
                paths = self.layout.path_options((value, n_value))
                if self.child is None:
                    self._route_dict[(value, n_value)] = len(paths[0])
                else:
                    a = paths[0]
                    a_path = self.child.shortest_path(a)
                    b = paths[-1]
                    b_path = self.child.shortest_path(b) if a != b else a_path
                    self._route_dict[(value, n_value)] = b_path if b_path < a_path else a_path

    def shortest_path(self, path: str) -> int:
        movements = "A" + path
        result = 0
        for i in range(len(movements) - 1):
            l = movements[i]
            r = movements[i + 1]
            result += self._route_dict[(l, r)]
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
        complexities.append(int(code[:3]) * keys)
    return sum(complexities)


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    arrows = 25 if part_b else 2
    return enter_keypad(source, arrows)
