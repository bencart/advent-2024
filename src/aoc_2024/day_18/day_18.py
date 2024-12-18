from heapq import heappop, heappush

from networkx import shortest_path

from aoc_2024.day_16.day_16_alt import build_graph
from common.input import get_data_file
from common.types import Coordinate, Grid

EXAMPLE = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def create_maze(
        data: str, size: tuple[int, int], ticks: int
) -> tuple[Grid, int, int, list[Coordinate]]:
    coords = [
        tuple(map(int, line.strip().split(",")))
        for line in data.strip().splitlines()
        if line.strip()
    ]
    grid = {(x, y): "." for x in range(size[0] + 1) for y in range(size[1] + 1)}
    grid[(0, 0)] = "S"
    grid[size] = "E"
    for i in range(ticks):
        grid[coords[i]] = "#"
    return grid, size[0] + 1, size[1] + 1, coords


def a_star(
        start: Coordinate, end: Coordinate, neighbors: Grid
) -> tuple[int, dict[Coordinate, Coordinate]]:
    heap = [(0, start)]
    g_cost = {start: 0}
    parent_map = {}

    while heap:
        score, position = heappop(heap)
        if position == end:
            return g_cost[end], parent_map

        for neighbor in neighbors.get(position, []):
            step_cost = g_cost[position] + 1
            if step_cost < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = step_cost
                parent_map[neighbor] = position
                heappush(heap, (step_cost, neighbor))
    return 0, parent_map


def backtrack_path(
        parent_map: dict[Coordinate, Coordinate], end: Coordinate
) -> list[Coordinate]:
    cells = []
    current = end
    while current in parent_map:
        cells.append(current)
        current = parent_map[current]
    return cells


def find_shortest_path(
        start: Coordinate, end: Coordinate, neighbor_grid: Grid
) -> Coordinate:
    cost, parents = a_star(start, end, neighbor_grid)
    path = backtrack_path(parents, end)
    return path


def shortest_path(data: str, size: tuple[int, int], ticks: int):
    grid, rows, cols, coords = create_maze(data, size, ticks)
    start, end, neighbor_grid = build_graph(grid)
    if ticks > 0:
        return len(find_shortest_path(start, end, neighbor_grid))
    else:
        path = [coords[0]]
        for coord in coords:
            del neighbor_grid[coord]
            if coord in path:
                path = find_shortest_path(start, end, neighbor_grid)
            if not path:
                return coord


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    grid = (6, 6) if example else (70, 70)
    ticks = 12 if example else 1024
    return shortest_path(source, grid, 0 if part_b else ticks)
