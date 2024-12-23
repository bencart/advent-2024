import importlib.util
import inspect
import os
from collections import defaultdict


def get_day_package_path(year: int) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", f"aoc_{year}")
    return os.path.normpath(relative_path)


def discover_main_methods(year: int = 2024):
    package_path = get_day_package_path(year)
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
                    p_name, m_name = (
                        module_name.split(".")
                        if "." in module_name
                        else (module_name, module_name)
                    )
                    day_number = p_name.split("_")[1] if "_" in p_name else 0

                    if name == "main":
                        main_methods.append(
                            {
                                "day": int(day_number),
                                "function": obj,
                                "main": True,
                                "alternate": len(m_name) > 6,
                                "path": f"{p_name}/{m_name}",
                            }
                        )
                    if name == "expected":
                        main_methods.append(
                            {
                                "day": int(day_number),
                                "function": obj,
                                "main": False,
                                "alternate": len(m_name) > 6,
                                "path": f"{p_name}/{m_name}",
                            }
                        )

    result = defaultdict(list)
    for main_method in main_methods:
        result[main_method["day"]].append(main_method)
    return result
