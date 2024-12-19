from common.constants import MOVEMENTS
from common.input import get_lines, get_data_file
from common.types import Grid, Coordinate

EXAMPLE = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

WALL = "#"
BOX = "O"
BOX_L = "["
BOX_R = "]"
BOXES = [BOX_L, BOX_R]
ROBOT = "@"
SPACE = "."
DIRECTIONS = ["^", ">", "v", "<"]
OFFSETS = {DIRECTIONS[k]: MOVEMENTS[k] for k in range(len(MOVEMENTS))}


def parse_input(data: str, wide: bool) -> tuple[Grid, list[str]]:
    input_data = data
    if wide:
        input_data = (
            input_data.replace(SPACE, "..")
            .replace(WALL, "##")
            .replace(BOX, "[]")
            .replace(ROBOT, "@.")
        )
    lines = get_lines(input_data)
    movements = []
    grid = {}
    for x, line in enumerate(lines):
        if line[0] == WALL:
            for y, s in enumerate(line):
                grid[(x, y)] = s
        else:
            movements += [m for m in line]
    return {k: v for k, v in grid.items() if v != SPACE}, movements


def single_axis_y(y: int, fixed: int):
    return fixed, y


def single_axis_x(x: int, fixed: int):
    return x, fixed


def sum_coordinate(a: Coordinate, b: Coordinate) -> Coordinate:
    return a[0] + b[0], a[1] + b[1]


def move_robot_along_axis(
    grid: Grid, start: int, delta: int, fixed: int, to_key: callable
) -> Coordinate:
    for coord in range(start, 0 if delta < 0 else len(grid), delta):
        key = to_key(coord, fixed)
        if key not in grid:
            for back_coord in range(coord, start, -delta):
                back_key = to_key(back_coord, fixed)
                prev_key = to_key(back_coord - delta, fixed)
                grid[back_key] = grid[prev_key]
            grid.pop(to_key(start, fixed))
            return to_key(start + delta, fixed)
        if grid[key] == WALL:
            break
    return to_key(start, fixed)


def move_robot_with_boxes(
    grid: Grid, start: Coordinate, delta: Coordinate
) -> Coordinate:
    desired = sum_coordinate(start, delta)
    up = delta[0] == -1
    movements = [start]
    boxes = {(start[1], start[1])}

    for new_x in range(desired[0], 0 if up else len(grid), delta[0]):
        new_ys = {y for box in boxes for y in box}
        any_walls = any([grid.get((new_x, y), SPACE) == WALL for y in new_ys])
        all_space = all([(new_x, y) not in grid for y in new_ys])

        if all_space:
            for move_from in reversed(movements):
                move_to = sum_coordinate(move_from, delta)
                grid[move_to] = grid.pop(move_from)
            return desired
        elif any_walls:
            return start

        new_boxes = {(new_x, y): grid.get((new_x, y), SPACE) for y in new_ys}
        boxes.clear()
        for position, box in new_boxes.items():
            if not box in BOXES:
                continue
            box = (
                (position[1], position[1] + 1)
                if box == BOX_L
                else (position[1] - 1, position[1])
            )
            boxes.add(box)
            if (new_x, box[0]) not in movements:
                movements.append((new_x, box[0]))
            if (new_x, box[1]) not in movements:
                movements.append((new_x, box[1]))

    return start


def update_grid(
    grid: Grid, robot: Coordinate, move: str, boxes: bool
) -> tuple[int, int]:
    dx, dy = OFFSETS[move]
    rx, ry = robot

    if dx != 0:
        if not boxes:
            return move_robot_along_axis(grid, rx, dx, ry, single_axis_x)
        else:
            return move_robot_with_boxes(grid, robot, (dx, dy))
    elif dy != 0:
        return move_robot_along_axis(grid, ry, dy, rx, single_axis_y)
    return rx, ry


def sum_gps_of_executed_plan(data: str, wide: bool) -> int:
    grid, moves = parse_input(data, wide)
    boxes = BOX_L in grid.values()
    robot = [k for k, v in grid.items() if v == ROBOT][0]
    for i, move in enumerate(moves):
        robot = update_grid(grid, robot, move, boxes)
    return sum(100 * k[0] + k[1] for k, v in grid.items() if v == BOX or v == BOX_L)


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    return sum_gps_of_executed_plan(source, part_b)
