from collections import defaultdict

from common.input import load_dict_grid, get_data_file

EXAMPLE = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


def get_fences(regions: dict[str, list]) -> dict[tuple, list]:
    result = defaultdict(list)
    for char, char_regions in regions.items():
        for region in char_regions:
            possible = 0
            for r, c in region:
                possible += 4
                top = (r - 1, c) in region
                lef = (r, c - 1) in region
                rig = (r, c + 1) in region
                bot = (r + 1, c) in region

                if top:
                    possible -= 1
                if lef:
                    possible -= 1
                if rig:
                    possible -= 1
                if bot:
                    possible -= 1
            result[char].append(possible)
    return result


def get_discount_fences(regions: dict[str, list]) -> dict[tuple, list]:
    result = defaultdict(list)
    for char, char_regions in regions.items():
        for region in char_regions:
            possible = 0
            for r, c in region:
                possible += 4
                top = (r - 1, c) in region
                lef = (r, c - 1) in region
                rig = (r, c + 1) in region
                bot = (r + 1, c) in region

                top_rig = (r - 1, c + 1) in region
                bot_lef = (r + 1, c - 1) in region

                if top or (rig and not top_rig):
                    possible -= 1
                if lef or (bot and not bot_lef):
                    possible -= 1
                if rig or (top and not top_rig):
                    possible -= 1
                if bot or (lef and not bot_lef):
                    possible -= 1
            result[char].append(possible)
    return result


def calculate_fence_price(data: str, discount: bool) -> int:
    grid, row_count, col_count = load_dict_grid(data)

    regions = defaultdict(list)

    for row in range(row_count):
        for col in range(col_count):
            index = (row, col)
            char = grid[index]
            this_region = {index}
            adj_indexes = {
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            }
            for region in regions[char]:
                if region & adj_indexes:
                    this_region.update(region)
            regions[char] = [r for r in regions[char] if not r & this_region]
            regions[char].append(this_region)

    price = 0

    fence_lookup = get_discount_fences(regions) if discount else get_fences(regions)

    for char, region_list in regions.items():
        for index, region in enumerate(region_list):
            fences = fence_lookup[char][index]
            area = len(region)
            price += area * fences
    return price


def main(day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(f"day_{day}.txt")
    return calculate_fence_price(source, part_b)
