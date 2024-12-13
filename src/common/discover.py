import importlib.util
import inspect
import os
from collections import defaultdict


def get_day_package_path() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "..", "days")
    return os.path.normpath(relative_path)


def discover_main_methods():
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
                    if name == "main":
                        package_name, module_name = module_name.split(".")
                        _, day_number = package_name.split("_")
                        main_methods.append(
                            {
                                "day": int(day_number),
                                "function": obj,
                                "alternate": len(module_name) > 6,
                            }
                        )
    result = defaultdict(list)
    for main_method in main_methods:
        result[main_method["day"]].append(main_method)
    return result
