import os
import sys
import subprocess
import shutil

import pytest


@pytest.mark.timeout(60)
def test_cli_where():
    strings = [
        rf'import is_odd  # instld: where {os.path.join("tests", "cli", "data", "pok")}',
        rf'import is_even  # instld: where {os.path.join("tests", "cli", "data", "chpok")}',
        'assert is_odd.valid(23)',
        'assert is_even.isEven(1)',
    ]

    script = os.path.join('tests', 'cli', 'data', 'main.py')
    with open(script, 'w') as file:
        file.write('\n'.join(strings))

    result = subprocess.run(['instld', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    result.check_returncode()

    base_libs_paths = {
        os.path.join('tests', 'cli', 'data', 'pok'): 'is_odd',
        os.path.join('tests', 'cli', 'data', 'chpok'): 'is_even',
    }

    for path, library_name in base_libs_paths.items():
        full_path_to_the_lib = os.path.join(path, 'lib')
        if sys.platform.lower() not in ('win32',):
            full_path_to_the_lib = os.path.join(full_path_to_the_lib, os.path.basename(os.listdir(path=full_path_to_the_lib)[0]), 'site-packages')
        full_path_to_the_lib = os.path.join(full_path_to_the_lib, library_name)

        assert os.path.isdir(full_path_to_the_lib)

        shutil.rmtree(path)

    os.remove(script)
