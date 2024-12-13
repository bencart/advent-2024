import importlib.util
import inspect
import os
from collections import defaultdict

from common.readme import write_header, write_lines


def get_day_package_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", "days")
    return os.path.normpath(relative_path)


def discover_main_methods(short: bool = True):
    if not short:
        print_readme()
    package_path = get_day_package_path()
    main_methods = []

    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_name = (
                    os.path.relpath(file_path, package_path)
                    .replace(os.sep, ".")
                    .rstrip(".py")
                )

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Error importing {module_name}: {e}")
                    continue
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    package_name, module_name = (
                        module_name.split(".")
                        if "." in module_name
                        else (module_name, module_name)
                    )
                    day_number = (
                        package_name.split("_")[1] if "_" in package_name else 0
                    )

                    if name == "main":
                        main_methods.append(
                            {
                                "day": int(day_number),
                                "function": obj,
                                "main": True,
                                "alternate": len(module_name) > 6,
                                "path": f"{package_name}/{module_name}",
                            }
                        )
                    if name == "expected":
                        main_methods.append(
                            {
                                "day": int(day_number),
                                "function": obj,
                                "main": False,
                                "alternate": len(module_name) > 6,
                                "path": f"{package_name}/{module_name}",
                            }
                        )

    result = defaultdict(list)
    for main_method in main_methods:
        result[main_method["day"]].append(main_method)
    return result


def print_readme():
    write_header()
    lines = []
    result = discover_main_methods()
    for i in range(len(result)):
        day = i + 1
        main = [r for r in result[day] if not r.get("alternate") and r.get("main")][0]
        alt = [r for r in result[day] if r.get("alternate") and r.get("main")]
        lines.append(
            f"{day}. https://github.com/bencart/advent-2024/blob/main/src/days/{main["path"]}.py"
        )
        if alt:
            for r in alt:
                lines.append(
                    f"    - https://github.com/bencart/advent-2024/blob/main/src/days/{r["path"]}.py"
                )

    lines.append("")
    lines.append("## My Output:")
    lines.append("")
    lines.append("```text")
    write_lines(lines)
