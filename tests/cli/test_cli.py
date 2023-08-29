import os
import sys
import json
import subprocess
import shutil

import pytest


@pytest.mark.timeout(120)
def test_cli_where(main_runner):
    strings = [
        rf'import is_odd  # instld: where {os.path.join("tests", "cli", "data", "pok")}',
        rf'import is_even  # instld: where {os.path.join("tests", "cli", "data", "chpok")}',
        'assert is_odd.valid(23)',
        'assert is_even.isEven(1)',
    ]

    script = os.path.join('tests', 'cli', 'data', 'main.py')
    with open(script, 'w') as file:
        file.write('\n'.join(strings))

    for runner in (main_runner, subprocess.run):
        result = runner(['instld', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10000)

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


def test_run_command_without_arguments(main_runner):
    for runner in (main_runner, subprocess.run):
        result = runner(['instld'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=100)

        assert result.returncode == 1
        assert result.stdout.decode('utf-8')  == ''
        assert result.stderr.decode('utf-8') == f'usage: instld python_file.py [argv ...]{os.linesep}'


def test_run_command_with_arguments(main_runner):
    strings = [
        'import json, sys',
        'print(json.dumps(sys.argv), file=sys.stdout)',
    ]

    script = os.path.join('tests', 'cli', 'data', 'main.py')
    with open(script, 'w') as file:
        file.write(os.linesep.join(strings))

    extra_arguments_options = (
        [],
        ['kek'],
        ['--lol', 'kek'],
        ['-l', 'kek'],
    )

    for runner in (main_runner, subprocess.run):
        for extra_arguments in extra_arguments_options:
            expected_arguments_without_command = [script] + extra_arguments
            result = runner(['instld', *expected_arguments_without_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=200)

            result.check_returncode()
            assert result.stderr.decode('utf-8') == ''

            arguments_from_file = json.loads(result.stdout.decode('utf-8'))
            arguments_from_file_without_command = arguments_from_file[1:]

            assert arguments_from_file_without_command == expected_arguments_without_command

    os.remove(script)


def test_exceptions_are_similar_with_just_python_command(main_runner):
    errors = [
        'ValueError',
        'ValueError("message")',
    ]

    for runner in (main_runner, subprocess.run):
        for error in errors:
            script = os.path.join('tests', 'cli', 'data', 'main.py')
            with open(script, 'w') as file:
                file.write(f'raise {error}')

            result_1 = runner(['instld', os.path.abspath(script)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=500)
            result_2 = subprocess.run(['python', os.path.abspath(script)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=500)

            assert result_1.returncode == result_2.returncode
            assert result_1.stdout == result_2.stdout
            assert result_1.stderr == result_2.stderr

            os.remove(script)
