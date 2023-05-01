import sys
import importlib
from contextlib import contextmanager
import copy


class Context:
    original_path = copy.copy(sys.path)

    def __init__(self, where):
        self.where = where

    def __str__(self):
        return f'<Context with path "{self.where}">'

    def __repr__(self):
        return f'{type(self).__name__}("{self.where}")'

    def import_here(self, module_name):
        with self.new_path():
            module = importlib.import_module(module_name)
            importlib.reload(module)
            return module

    @contextmanager
    def new_path(self):
        old_path = sys.path
        sys.path = [self.where] + copy.copy(self.original_path)
        importlib.invalidate_caches()
        yield
        sys.path = old_path
        importlib.invalidate_caches()
