import sys
import importlib
from contextlib import contextmanager
import copy

from instld.module.lock import lock
from instld.common_utils.convert_options import convert_options


class Context:
    original_path = copy.copy(sys.path)

    def __init__(self, where, logger, catch_output, options, installer):
        self.where = where
        self.logger = logger
        self.catch_output = catch_output
        self.options = options
        self.installer = installer

    def __str__(self):
        return f'<Context with path "{self.where}">'

    def __repr__(self):
        return f'{type(self).__name__}("{self.where}")'

    def import_here(self, module_name, *args, **kwargs):
        with lock:
            with self.new_path(module_name):
                self.logger.info(f'importing "{module_name}" from "{self.where}", sys.path now is: {sys.path}')
                module = importlib.import_module(module_name, *args, **kwargs)
                importlib.reload(module)
                return module

    @contextmanager
    def new_path(self, module_name):
        old_path = sys.path
        sys.path = [self.where] + copy.copy(self.original_path)
        if module_name in sys.modules:
            sys.modules.pop(module_name)
        yield
        sys.path = old_path

    def install(self, *package_names, catch_output=False, **options):
        if not package_names:
            raise ValueError('You need to pass at least one package name.')

        options = convert_options(options)
        with self.installer(package_names, catch_output=catch_output, options=options):
            pass
