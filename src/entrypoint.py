from common.discover import discover_main_methods
from common.execution import execute_day_methods

if __name__ == "__main__":
    ONLY_TODAY = False
    main_methods = discover_main_methods()

    for day in sorted(main_methods.keys()):
        if not ONLY_TODAY or day == len(main_methods):
            execute_day_methods(day, main_methods[day], len(main_methods))
