import sys
import builtins
import importlib
import inspect
import argparse
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from threading import Lock

import installed
from installed.errors import InstallingPackageError
from installed.cli.get_comment_string import get_comment_string


def get_options_from_comments(frame):
    frame = frame.f_back
    comment_string = get_comment_string(frame)

    result = {}

    if comment_string is not None:
        options = (x.strip() for x in comment_string.split(','))
        options = (x for x in options if x)

        for option in options:
            splitted_option = [x for x in option.split() if x]

            if len(splitted_option) != 2:
                raise InstallingPackageError()

            option_name = splitted_option[0].strip().lower()
            option_value = splitted_option[1].strip().lower()
            result[option_name] = option_value

    return result

def start():
    with installed() as context:
        lock = Lock()
        old_import = builtins.__import__

        @contextmanager
        def set_import():
            builtins.__import__ = old_import
            yield
            builtins.__import__ = import_wrapper

        def import_wrapper(name, *args, **kwargs):
            splitted_name = name.split('.')
            base_name = splitted_name[0]
            base_sequence = '.'.join(splitted_name[:-1])
            last_name = splitted_name[-1]

            current_frame = inspect.currentframe()
            options = get_options_from_comments(current_frame)

            if 'package' in options:
                package_name = options['package']
            else:
                package_name = base_name

            if 'version' in options:
                package_name = f'{package_name}=={options["version"]}'

            with lock:
                with set_import():
                    try:
                        result = __import__(name, *args, **kwargs)
                    except (ModuleNotFoundError, ImportError):
                        context.install(package_name)
                        result = context.import_here(base_name)
                        sys.modules[base_name] = result

                    if 'fromlist' in kwargs and kwargs['fromlist']:
                        if len(splitted_name) > 1:
                            for index, subname in enumerate(splitted_name):
                                if index:
                                    try:
                                        result = getattr(result, subname)
                                    except AttributeError:
                                        raise ImportError(f"cannot import name '{last_name}' from '{base_sequence}'")

                    return result

    builtins.__import__ = import_wrapper

    parser = argparse.ArgumentParser(description='Running a script with automatic installation of dependencies.')
    parser.add_argument('python_file', type=str, help='The path to the file with the extension ".py" containing Python code.')
    arguments = parser.parse_args()

    spec = importlib.util.spec_from_file_location('kek', arguments.python_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules['__main__'] = module
    spec.loader.exec_module(module)


if __name__ == "__main__":
    start()
