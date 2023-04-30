import os
from tempfile import TemporaryDirectory
from modulefinder import ModuleFinder


class PackageWrapper:
    def __init__(self, where):
        self.where = where

    def import_here(self, module_name):
        with TemporaryDirectory() as directory:
            file_name = os.path.join(directory, 'file.py')
            with open(file_name, 'w') as file:
                file.write(f'import {module_name}')

            finder = ModuleFinder(path=[self.where])
            finder.run_script(file_name)
            return finder.modules[module_name]
