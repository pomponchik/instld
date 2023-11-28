import os
import sys
import tempfile
from functools import partial

from contextlib import contextmanager

from instld.errors import InstallingPackageError, RunningCommandError
from instld.module.context import Context
from instld.module.runner import run_python as standard_runner
from instld.module.lock import lock


@contextmanager
def search_path(base_dir, logger, runner):
    sys_path = os.path.join(base_dir, 'lib')

    standard_runner(['-m', 'venv', base_dir], logger, True)

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
def pip_context(packages_names, options, logger, runner, catch_output, where):
    if where is not None:
        @contextmanager
        def create_temp_directory():
            yield where
    else:
        create_temp_directory = tempfile.TemporaryDirectory
    with create_temp_directory() as directory:
        with search_path(directory, logger, runner) as where:
            try:
                if '-r' in options or '--requirement' in options:
                    runner(['-m', 'pip', 'install', f'--target={where}', *options], logger, catch_output)
                else:
                    for package_name in packages_names:
                        runner(['-m', 'pip', 'install', f'--target={where}', *options, package_name], logger, catch_output)
            except RunningCommandError as e:
                new_error = InstallingPackageError(f'{str(e)} It occurred when installing one of the following packages: {", ".join(packages_names)}.')
                new_error.stdout = e.stdout
                new_error.stderr = e.stderr
                raise new_error from e

            yield Context(where, logger, catch_output, options, partial(pip_context, logger=logger, runner=runner, catch_output=catch_output, where=directory))
