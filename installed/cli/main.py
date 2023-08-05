import sys
import builtins
import importlib
import inspect
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from threading import Lock

import installed
from installed.cli.parsing_comments.get_options_from_comments import get_options_from_comments
from installed.cli.parsing_arguments.get_arguments import get_arguments


def start():
    arguments = get_arguments()

    with installed() as context:
        lock = Lock()
        old_import = builtins.__import__
        locations = {}

        @contextmanager
        def set_import():
            builtins.__import__ = old_import
            yield
            builtins.__import__ = import_wrapper

        def get_current_context(where):
            if where is None:
                return context

            else:
                with lock:
                    location_context = locations.get(where)
                    if location_context is not None:
                        return location_context[1]

                    manager = installed(where=where)
                    local_context = manager.__enter__()
                    locations[where] = (manager, local_context)
                    return local_context

        def import_wrapper(name, *args, **kwargs):
            splitted_name = name.split('.')
            base_name = splitted_name[0]
            base_sequence = '.'.join(splitted_name[:-1])
            last_name = splitted_name[-1]

            current_frame = inspect.currentframe()
            options = get_options_from_comments(current_frame.f_back)

            package_name = options.pop('package', base_name)

            if 'version' in options:
                package_name = f'{package_name}=={options.pop("version")}'

            current_context = get_current_context(options.pop('where', None))

            with lock:
                with set_import():
                    try:
                        result = __import__(name, *args, **kwargs)
                    except (ModuleNotFoundError, ImportError) as e:
                        current_context.install(package_name)
                        result = current_context.import_here(base_name)
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

    spec = importlib.util.spec_from_file_location('kek', arguments.python_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules['__main__'] = module
    spec.loader.exec_module(module)


if __name__ == "__main__":
    start()
