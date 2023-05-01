import os
import sys
import tempfile
import subprocess

from threading import Lock
from io import StringIO
from contextlib import contextmanager

from installed.errors import InstallingPackageError
from installed.context import Context
from installed.runner import run_python as standard_runner


lock = Lock()

@contextmanager
def search_path(base_dir, logger, runner):
    path_to_venv = os.path.join(base_dir, 'venv')
    sys_path = os.path.join(path_to_venv, 'lib')

    standard_runner(['-m', 'venv', path_to_venv], logger)

    for maybe_directory in os.listdir(path=sys_path):
        maybe_directory_full = os.path.join(sys_path, maybe_directory)
        if maybe_directory.startswith('python') and os.path.isdir(maybe_directory_full):
            sys_path = os.path.join(sys_path, maybe_directory, 'site-packages')
            break

    with lock:
        sys.path.insert(0, sys_path)

    yield sys_path

    with lock:
        del sys.path[sys.path.index(sys_path)]

@contextmanager
def pip_context(packages_names, options, logger, runner):
    with tempfile.TemporaryDirectory() as directory:
        with search_path(directory, logger, runner) as where:
            try:
                for package_name in packages_names:
                    runner(['-m', 'pip', 'install', f'--target={where}', *options, package_name], logger)
            except subprocess.CalledProcessError as e:
                raise InstallingPackageError from e

            yield Context(where)
