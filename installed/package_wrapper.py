import sys
import importlib
from contextlib import contextmanager
import copy


class PackageWrapper:
    original_path = copy.copy(sys.path)

    def __init__(self, where):
        self.where = where

    def __str__(self):
        return f'<PackageWrapper with path "{self.where}">'

    def import_here(self, module_name):
        with self.new_path():
            module = importlib.import_module(module_name)
            importlib.reload(module)
            return module

    @contextmanager
    def new_path(self):
        old_path = sys.path
        sys.path = [self.where] + copy.copy(self.original_path)
        yield
        sys.path = old_path
