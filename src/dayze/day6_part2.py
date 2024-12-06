from common.input import get_data_file

MOVEMENTS = {"^": (-1, 0, ">"), ">": (0, 1, "v"), "v": (1, 0, "<"), "<": (0, -1, "^")}


def load_grid(data: str) -> list[list[str]]:
    lines = data.strip().split("\n")
    grid = [line for line in lines if line.strip()]
    return [[c for c in row] for row in grid]


def remove_guard(grid: list[list[str]]) -> (int, int, str):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            item = grid[row][col]
            if item in "^><v":
                grid[row][col] = "."
                return row, col, item


def is_outside_grid(grid: list[list[str]], row: int, col: int) -> bool:
    return row < 0 or col < 0 or row >= len(grid) or col >= len(grid[row])


def traverse_grid(
    grid: list[list[str]],
    row: int,
    col: int,
    direction: str,
    starting_locations: set[tuple[int, int]],
    starting_vectors: set[tuple[int, int, str]],
) -> (set[(int, int)], bool):
    visited_locations = {sl for sl in starting_locations}
    visited_vectors = {sv for sv in starting_vectors}
    visited_locations.add((row, col))
    visited_vectors.add((row, col, direction))

    cur_row, cur_col, cur_dir = row, col, direction
    move_row, move_col, turn_dir = MOVEMENTS[cur_dir]
    while True:
        next_row, next_col = cur_row + move_row, cur_col + move_col

        if (
            next_row < 0
            or next_col < 0
            or next_row >= len(grid)
            or next_col >= len(grid[next_row])
        ):
            return visited_locations, False

        if grid[next_row][next_col] == "#":
            cur_dir = turn_dir
            move_row, move_col, turn_dir = MOVEMENTS[cur_dir]
            vector = (cur_row, cur_col, cur_dir)
            if vector in visited_vectors:
                return visited_locations, True
            visited_vectors.add(vector)
            continue

        visited_locations.add((next_row, next_col))
        cur_row, cur_col = next_row, next_col

        vector = (cur_row, cur_col, cur_dir)
        if vector in visited_vectors:
            return visited_locations, True
        visited_vectors.add(vector)


def step_branch_traverse(
    grid: list[list[str]], row: int, col: int, direction: str
) -> int:
    visited_locations = {(row, col)}
    visited_vectors = {(row, col, direction)}
    count = 0

    cur_row, cur_col, cur_dir = row, col, direction
    move_row, move_col, turn_dir = MOVEMENTS[cur_dir]
    while True:
        next_row, next_col = cur_row + move_row, cur_col + move_col

        if (
            next_row < 0
            or next_col < 0
            or next_row >= len(grid)
            or next_col >= len(grid[next_row])
        ):
            return count

        if grid[next_row][next_col] == "#":
            cur_dir = turn_dir
            move_row, move_col, turn_dir = MOVEMENTS[cur_dir]
            continue

        if (next_row, next_col) not in visited_locations:
            grid[next_row][next_col] = "#"
            _, stuck = traverse_grid(
                grid, cur_row, cur_col, turn_dir, visited_locations, visited_vectors
            )
            grid[next_row][next_col] = "."  # Restore grid
            count += 1 if stuck else 0

        visited_locations.add((next_row, next_col))
        cur_row, cur_col = next_row, next_col


def find_loop_options(data: str) -> int:
    grid = load_grid(data)
    row, col, direction = remove_guard(grid)
    count = step_branch_traverse(grid, row, col, direction)
    return count


def count_visited_locations(data: str) -> int:
    grid = load_grid(data)
    row, col, direction = remove_guard(grid)
    unique_locations, _ = traverse_grid(grid, row, col, direction, set(), set())
    return len(unique_locations)


def main(example: str, data_file: str) -> None:
    print(f"Day 6 Part A Example = {count_visited_locations(example)}")
    part_a = get_data_file(data_file)
    print(f"Day 6 Part A = {count_visited_locations(part_a)}")

    print(f"Day 6 Part B Example = {find_loop_options(example)}")
    part_b = get_data_file(data_file)
    print(f"Day 6 Part B = {find_loop_options(part_b)}")
