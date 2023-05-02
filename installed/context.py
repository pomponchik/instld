import sys
import importlib
from contextlib import contextmanager
import copy

from installed.lock import lock


class Context:
    original_path = copy.copy(sys.path)

    def __init__(self, where, logger):
        self.where = where
        self.logger = logger

    def __str__(self):
        return f'<Context with path "{self.where}">'

    def __repr__(self):
        return f'{type(self).__name__}("{self.where}")'

    def import_here(self, module_name):
        with lock:
            with self.new_path(module_name):
                self.logger.info(f'importing "{module_name}" from "{self.where}", sys.path now is: {sys.path}')
                module = importlib.import_module(module_name)
                importlib.reload(module)
                return module

    @contextmanager
    def new_path(self, module_name):
        old_path = sys.path
        sys.path = [self.where] + copy.copy(self.original_path)
        if module_name in sys.modules:
            old_module = sys.modules.pop(module_name)
        else:
            old_module = None
        yield
        sys.path = old_path
