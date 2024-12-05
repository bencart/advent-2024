import os


def get_data_file_path(file_name: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", "..", "data", file_name)
    return os.path.normpath(relative_path)


def get_data_file(file_name: str) -> str:
    path = get_data_file_path(file_name)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading the file: {e}")
    else:
        print(f"File does not exist: {path}")


def get_data(data: str, column: bool = False):
    lines = data.strip().split("\n")
    rows = [list(map(int, line.split())) for line in lines]
    if not column:
        return rows
    columns = list(zip(*rows))
    return [list(col) for col in columns]
