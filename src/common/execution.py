import time


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
):
    start_time = time.time()
    result = func(day=day, example=example, part_b=part_b)
    end_time = time.time()
    execution_time = format_execution_time(end_time - start_time)

    part = "B" if part_b else "A"
    alternate = "*" if alternate else " "
    exec_type = "Example " if example else "        "

    print(
        f"Day {format_day(day)} Part {part} {exec_type} {alternate} Execution Time: {execution_time} Result : {result}"
    )
    return result


def execute_day(
    func: callable, day: int, current_day: int, got_butt_kicked: bool, alternate: bool
):
    redirect_and_time(func, day, True, False, alternate)
    redirect_and_time(func, day, False, False, alternate)

    if not got_butt_kicked or alternate:
        redirect_and_time(func, day, True, True, alternate)
        redirect_and_time(func, day, False, True, alternate)


def execute_day_methods(day: int, day_methods: list[dict[str, any]], days: int):
    for day_method in day_methods:
        main_method = day_method.get("function")
        if not day_method.get("alternate"):
            execute_day(main_method, day, days, len(day_methods) > 1, False)
    for day_method in day_methods:
        main_method = day_method.get("function")
        if day_method.get("alternate"):
            execute_day(main_method, day, days, len(day_methods) > 1, True)
