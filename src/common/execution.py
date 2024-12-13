import time

from common.discover import discover_main_methods
from common.readme import (
    write_readme_header,
    write_readme_solution_links,
    write_readme_output_header,
    write_readme_footer,
    write_readme_result
)


def format_execution_time(seconds: float) -> str:
    """Format execution time in milliseconds or seconds."""
    return (f"{seconds * 1000:.2f} ms" if seconds < 1 else f"{seconds:.2f}  s").rjust(
        11
    )


def format_day(day: int) -> str:
    """Format day number with left padding."""
    return str(day).rjust(2)


def redirect_and_time(
    func: callable,
    day: int,
    example: bool,
    part_b: bool,
    alternate: bool = False,
    only_today: bool = False,
    expected_value: int = None,
):
    start_time = time.time()
    result = func(day=day, example=example, part_b=part_b)
    accurate = ""
    if expected_value is not None and result == expected_value:
        accurate = " ✅"
    elif expected_value is not None:
        accurate = " "

    end_time = time.time()
    execution_time = format_execution_time(end_time - start_time)

    part = "B" if part_b else "A"
    alternate = "*" if alternate else " "
    exec_type = "Example " if example else "        "

    output = f"Day {format_day(day)} Part {part} {exec_type} {alternate} Execution Time: {execution_time} Result : {result} {accurate}"
    if not only_today:
        write_readme_result(output)
    print(output)
    return result


def execute_day(
    func: callable,
    day: int,
    current_day: int,
    got_butt_kicked: bool,
    alternate: bool,
    expected: callable,
    only_today: bool,
):
    expected_value = expected(False) if expected else None
    redirect_and_time(func, day, True, False, alternate, only_today, expected_value)
    redirect_and_time(func, day, False, False, alternate, only_today)

    if not got_butt_kicked or alternate:
        expected_value = expected(True) if expected else None
        redirect_and_time(func, day, True, True, alternate, only_today, expected_value)
        redirect_and_time(func, day, False, True, alternate, only_today)


def execute_day_methods(
    day: int, day_methods: list[dict[str, any]], days: int, only_today: bool
):
    expected_method = None
    bad_day = False
    for day_method in day_methods:
        if not day_method.get("main"):
            expected_method = day_method.get("function")
        bad_day |= day_method.get("main") and day_method.get("alternate")

    for day_method in day_methods:
        main_method = day_method.get("function")
        if not day_method.get("alternate") and day_method.get("main"):
            execute_day(
                main_method, day, days, bad_day, False, expected_method, only_today
            )
    for day_method in day_methods:
        main_method = day_method.get("function")
        if day_method.get("alternate") and day_method.get("main"):
            execute_day(
                main_method, day, days, bad_day, True, expected_method, only_today
            )


def execute_advent(only_today: bool):
    if not only_today:
        write_readme_header()

    main_methods = discover_main_methods()

    if not only_today:
        write_readme_solution_links(main_methods)
        write_readme_output_header()

    for day in sorted(main_methods.keys()):
        if not only_today or day == len(main_methods):
            execute_day_methods(day, main_methods[day], len(main_methods), only_today)

    if not only_today:
        write_readme_footer()
