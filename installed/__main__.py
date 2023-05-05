import sys
import builtins
import importlib.util
from contextlib import contextmanager
from tempfile import TemporaryDirectory

import installed




def start():
    with installed() as context:
        old_import = builtins.__import__

        @contextmanager
        def set_import():
            builtins.__import__ = old_import
            yield
            builtins.__import__ = import_wrapper

        def import_wrapper(name, *args, **kwargs):
            with set_import():
                try:
                    result = __import__(name, *args, **kwargs)
                except (ModuleNotFoundError, ImportError):
                    context.install(name.split('.')[0])
                    result = context.import_here(name.split('.')[0])
                    sys.modules[name.split('.')[0]] = result

                if 'fromlist' in kwargs and kwargs['fromlist']:
                    if len(name.split('.')) > 1:
                        for index, subname in enumerate(name.split('.')):
                            if index:
                                result = getattr(result, subname)

                return result

    builtins.__import__ = import_wrapper

    spec = importlib.util.spec_from_file_location('kek', sys.argv[1])
    module = importlib.util.module_from_spec(spec)
    sys.modules['__main__'] = module
    spec.loader.exec_module(module)




if __name__ == "__main__":
    start()
