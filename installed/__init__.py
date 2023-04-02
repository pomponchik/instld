import os
import sys
import tempfile
import subprocess
from threading import Lock
from io import StringIO
from contextlib import contextmanager


class InstallingPackageError(subprocess.CalledProcessError):
    pass
    

lock = Lock()


@contextmanager
def search_path(base_dir):
    path_to_venv = os.path.join(base_dir, 'venv')
    sys_path = os.path.join(path_to_venv, 'lib', 'python3.9', 'site-packages')

    subprocess.check_call([sys.executable, '-m', 'venv', path_to_venv], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    sys.path.append(sys_path)

    yield sys_path

    del sys.path[sys.path.index(sys_path)]

@contextmanager
def pip_context(package_name):
    with lock:
        with tempfile.TemporaryDirectory() as directory:
            with search_path(directory) as where:
                try:

                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', f'--target={where}', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except subprocess.CalledProcessError as e:
                    raise InstallingPackageError from e

                yield


class ProxyModule(sys.modules[__name__].__class__):
    def __call__(self, package_name):
        return pip_context(package_name)

sys.modules[__name__].__class__ = ProxyModule
