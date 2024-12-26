from common.input import get_data_file

EXAMPLE = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def parse_input(data: str):
    items = data.strip().split("\n\n")
    keys = []
    locks = []
    for item in items:
        lines = item.strip().split("\n")
        key_lock = [-1] * len(lines[0])
        for line in lines:
            for i, c in enumerate(line.strip()):
                key_lock[i] += 1 if c == "#" else 0
        if lines[0] == "." * len(lines[0]):
            keys.append(key_lock)
        else:
            locks.append(key_lock)
    return locks, keys


def find_lock_keys(data: str):
    locks, keys = parse_input(data)
    combos = 0
    for lock in locks:
        for key in keys:
            combo = [key[i] + lock[i] for i in range(len(key))]
            valid = all(c < 6 for c in combo)
            combos += 1 if valid else 0
    return combos


def main(year: int, day: int, example: bool, part_b: bool) -> any:
    if part_b:
        return
    source = EXAMPLE if example else get_data_file(year, day)
    return find_lock_keys(source)
