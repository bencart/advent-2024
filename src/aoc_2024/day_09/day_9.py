from common.input import get_data_file


EXAMPLE = "2333133121414131402"


def represent_disk(file_layout: str) -> list[str | int]:
    index = 0
    is_on = True
    disk = []
    for length in file_layout:
        if is_on:
            disk += int(length) * [index]
            is_on = False
            index += 1
        else:
            disk += int(length) * ["."]
            is_on = True
    return disk


def compact_files(data: list[str | int]) -> list[str | int]:
    disk = [i for i in data]
    compacted = []
    head = 0
    tail = len(disk) - 1

    while head < len(disk):
        if disk[head] != ".":
            compacted.append(disk[head])
        else:
            while tail > head and disk[tail] == ".":
                tail -= 1
            if tail > head:
                compacted.append(disk[tail])
                disk[tail] = "."
                tail -= 1
            else:
                compacted.append(".")
        head += 1
    return compacted


def defragment_files(data: str) -> list[int | str]:
    space = []
    files = []

    key = 0
    index = 0
    empty = False
    for block in data:
        size = int(block)
        if not empty:
            files.append([index, size, key])
            key += 1
        else:
            space.append([index, size])
        index += size
        empty = not empty

    for file_info in reversed(files):
        file_index = file_info[0]
        file_size = file_info[1]
        for space_info in space:
            space_index = space_info[0]
            space_size = space_info[1]

            if file_size <= space_size and file_index > space_index:
                file_info[0] = space_index
                space_info[0] = space_index + file_size
                space_info[1] = space_size - file_size
                break

    sorted_files = sorted(files, key=lambda file: file[0])
    result = []
    for file in sorted_files:
        if len(result) != file[0]:
            result.extend("." for _ in range(file[0] - len(result)))
        result.extend(file[2] for _ in range(file[1]))
    return result


def compact_and_checksum(data: str, defrag: bool = False) -> int:
    file_layout = data.strip()
    if not defrag:
        expanded = represent_disk(file_layout)
        compacted = compact_files(expanded)
    else:
        compacted = defragment_files(file_layout)
    return sum([i * v for i, v in enumerate(compacted) if v != "."])


def main(year: int, day: int, example: bool, part_b: bool) -> int:
    source = EXAMPLE if example else get_data_file(year, day)
    return compact_and_checksum(source, defrag=part_b)
