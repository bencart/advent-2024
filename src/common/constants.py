import os
from datetime import datetime

MOVEMENTS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
ADJACENT = set(MOVEMENTS)
CORRECT = "✅"
WRONG = "❌"
YEAR = datetime.now().year
URL_TEMPLATE = "https://adventofcode.com/{year}/day/{day}/input"
COOKIE = os.environ.get("COOKIE")
