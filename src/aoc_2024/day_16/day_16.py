from networkx import Graph, shortest_path
from networkx.classes import all_neighbors

from common.constants import ADJACENT
from common.input import get_lines, get_data_file, load_dict_grid
from common.types import Grid, Coordinate

EXAMPLE_1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

EXAMPLE_2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

DELTA_DIR = {(-1, 0): "^", (1, 0): "v", (0, -1): "<", (0, 1): ">"}


def parse_input(data: str) -> Grid:
    lines = get_lines(data)
    grid = {}
    for x, line in enumerate(lines):
        for y, s in enumerate(line):
            grid[(x, y)] = s
    return grid


def sum_c(a: Coordinate, b: Coordinate) -> Coordinate:
    return a[0] + b[0], a[1] + b[1]


def dif_c(a: Coordinate, b: Coordinate) -> Coordinate:
    return a[0] - b[0], a[1] - b[1]


def calculate_cost(path: list[Coordinate], stop: int) -> int:
    current_direction = 0, 1
    cost = 0
    for i, node in enumerate(path):
        if stop is not None and cost > stop:
            return stop
        if i == 0:
            continue
        p = path[i - 1]
        d = sum_c(p, current_direction)
        if node == d:
            cost += 1
        else:
            cost += 1001
            current_direction = dif_c(node, p)
    return cost


def build_graph(grid: Grid) -> tuple[tuple, tuple, Graph]:
    start = None
    end = None
    graph = Graph()
    for k, v in grid.items():
        x, y = k
        if v in [".", "S", "E"]:
            for dir in [">", "<", "^", "v"]:
                graph.add_node((x, y, dir))
            graph.add_edge((x, y, ">"), (x, y, "^"), weight=1000)
            graph.add_edge((x, y, "<"), (x, y, "v"), weight=1000)
            graph.add_edge((x, y, ">"), (x, y, "v"), weight=1000)
            graph.add_edge((x, y, "<"), (x, y, "^"), weight=1000)
        if v == "S":
            start = (x, y, ">")
        elif v == "E":
            graph.add_node((x, y, None))
            for d in [">", "<", "^", "v"]:
                graph.add_edge((x, y, d), (x, y, None), weight=0)
            end = (x, y, None)
    for k, v in grid.items():
        if v == "#":
            continue
        for delta in ADJACENT:
            d = sum_c(k, delta)
            dir = DELTA_DIR[delta]
            if grid.get(d, "#") != "#":
                graph.add_edge((k[0], k[1], dir), (d[0], d[1], dir), weight=1)
    return start, end, graph


def calculate_cost(path: list[tuple]):
    cost = 0
    for i in range(1, len(path)):
        node = path[i]
        prev = path[i - 1]
        nx, ny, nd = node
        px, py, pd = prev
        if nd == None:
            cost += 0
        elif nd != pd:
            cost += 1000
        else:
            cost += 1
    return cost


def shortest_route(data: str, count_tiles: int):
    grid, rows, cols = load_dict_grid(data)
    start, end, graph = build_graph(grid)
    if not count_tiles:
        path = shortest_path(graph, start, end, weight="weight")
        return calculate_cost(path)
    else:

        def noo(x: tuple[int, int, int]) -> tuple[int, int]:
            return x[0], x[1]

        stack = [start]
        finished = {start}
        good_seats = {noo(start), noo(end)}
        optimal_path = shortest_path(graph, start, end, weight="weight")
        cost = calculate_cost(optimal_path)

        while stack:
            position = stack.pop()
            for neighbor in all_neighbors(graph, position):
                if neighbor in finished:
                    continue
                source_cost = cost
                target_cost = 0
                if neighbor not in optimal_path:
                    source_path = shortest_path(graph, start, neighbor, weight="weight")
                    target_path = shortest_path(graph, neighbor, end, weight="weight")
                    source_cost = calculate_cost(source_path)
                    target_cost = calculate_cost(target_path)
                if source_cost + target_cost == cost:
                    good_seats.add(neighbor)
                    stack.append(neighbor)
                finished.add(neighbor)
        return len({noo(gs) for gs in good_seats})


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    if example:
        small = shortest_route(EXAMPLE_1, part_b)
        large = shortest_route(EXAMPLE_2, part_b)
        return (small, large)
    return shortest_route(get_data_file(year, day), part_b)


if __name__ == "__main__":
    print(main(2024, 16, False, True))
