import io
import time
from contextlib import redirect_stdout

from common.constants import YEAR
from common.discover import discover_main_methods
from common.readme import (
    write_readme_header,
    write_readme_solution_links,
    write_readme_output_header,
    write_readme_footer,
    write_readme_result,
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
    year: int,
    day: int,
    example: bool,
    part_b: bool,
    alternate: bool = False,
    write_readme: bool = False,
    suppres_output: bool = False,
    expected_value: int = None,
):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        start_time = time.time()
        result = func(year=year, day=day, example=example, part_b=part_b)
    if not suppres_output:
        print(buffer.getvalue())

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
    if write_readme:
        write_readme_result(output)
    print(output)
    return result


def execute_day(
    func: callable,
    year: int,
    day: int,
    current_day: int,
    got_butt_kicked: bool,
    alt: bool,
    expected: callable,
    readme: bool,
):
    result = expected(False) if expected else None
    suppress = day != current_day
    redirect_and_time(func, year, day, True, False, alt, readme, suppress, result)
    redirect_and_time(func, year, day, False, False, alt, readme, suppress)

    if not got_butt_kicked or alt:
        result = expected(True) if expected else None
        redirect_and_time(func, year, day, True, True, alt, readme, suppress, result)
        redirect_and_time(func, year, day, False, True, alt, readme, suppress)


def execute_day_methods(
    year: int,
    day: int,
    day_methods: list[dict[str, any]],
    days: int,
    write_readme: bool,
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
                main_method,
                year,
                day,
                days,
                bad_day,
                False,
                expected_method,
                write_readme,
            )
    for day_method in day_methods:
        main_method = day_method.get("function")
        if day_method.get("alternate") and day_method.get("main"):
            execute_day(
                main_method,
                year,
                day,
                days,
                bad_day,
                True,
                expected_method,
                write_readme,
            )


def execute_advent(only_today: bool, year: int = YEAR):
    write_readme = year == YEAR and not only_today
    if write_readme:
        write_readme_header()

    main_methods = discover_main_methods(year)

    if write_readme:
        write_readme_solution_links(main_methods)
        write_readme_output_header()

    for day in sorted(main_methods.keys()):
        if not only_today or day == len(main_methods):
            execute_day_methods(
                year, day, main_methods[day], len(main_methods), write_readme
            )

    if write_readme:
        write_readme_footer()
