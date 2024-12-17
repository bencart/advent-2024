from heapq import heappop, heappush

from aoc_2024.day_16.day_16 import EXAMPLE_1, EXAMPLE_2, sum_c, dif_c
from common.constants import ADJACENT
from common.input import get_data_file, load_dict_grid
from common.types import Grid, Coordinate


def build_graph(grid: Grid) -> tuple[Coordinate, Coordinate, Grid]:
    start, end = None, None
    graph = {}

    for coord, value in grid.items():
        if value in {".", "S", "E"}:
            graph[coord] = [
                sum_c(coord, delta)
                for delta in ADJACENT
                if grid.get(sum_c(coord, delta), "#") != "#"
            ]
            if value == "S":
                start = coord
            elif value == "E":
                end = coord
    return start, end, graph


def a_star(
        start: Coordinate, end: Coordinate, direction: Coordinate, neighbors: Grid
) -> tuple[int, Coordinate, dict[Coordinate, Coordinate]]:
    heap = [(0, start, direction)]
    g_cost = {start: 0}
    parent_map = {}

    while heap:
        score, position, direction = heappop(heap)
        if position == end:
            return g_cost[end], direction, parent_map

        for neighbor in neighbors[position]:
            new_direction = dif_c(neighbor, position)
            step_cost = g_cost[position] + (1001 if direction != new_direction else 1)
            if step_cost < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = step_cost
                parent_map[neighbor] = position
                heappush(heap, (step_cost, neighbor, new_direction))

    return 0, direction, parent_map


def find_good_seats(
        start: Coordinate,
        end: Coordinate,
        start_dir: Coordinate,
        neighbors: Grid,
        cost: int,
        optimal_path: list[Coordinate],
) -> set[Coordinate]:
    stack = [start]
    finished = {start}
    good_seats = {start, end}

    while stack:
        position = stack.pop()
        for neighbor in neighbors[position]:
            if neighbor in finished:
                continue
            source_cost = cost
            target_cost = 0
            if neighbor not in optimal_path:
                source_cost, next_dir, _ = a_star(start, neighbor, start_dir, neighbors)
                target_cost, _, _ = a_star(neighbor, end, next_dir, neighbors)
            if source_cost + target_cost == cost:
                good_seats.add(neighbor)
                stack.append(neighbor)
            finished.add(neighbor)
    return good_seats


def backtrack_path(
        parent_map: dict[Coordinate, Coordinate], end: Coordinate
) -> list[Coordinate]:
    cells = []
    current = end
    while current in parent_map:
        cells.append(current)
        current = parent_map[current]
    return cells


def shortest_route(data: str, find_seats: bool):
    grid, rows, cols = load_dict_grid(data)
    start, end, neighbor_grid = build_graph(grid)
    start = [k for k, v in grid.items() if v == "S"][0]
    end = [k for k, v in grid.items() if v == "E"][0]
    g_cost, _, parent_map = a_star(start, end, (0, 1), neighbor_grid)
    if not find_seats:
        return g_cost
    optimal_path = backtrack_path(parent_map, end)
    cells = find_good_seats(start, end, (0, 1), neighbor_grid, g_cost, optimal_path)
    return len(cells)


def main(year: int, day: int, example: bool, part_b: bool) -> any:
    if example:
        small = shortest_route(EXAMPLE_1, part_b)
        large = shortest_route(EXAMPLE_2, part_b)
        return small, large
    return shortest_route(get_data_file(year, day), part_b)
