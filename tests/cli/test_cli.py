import os
import subprocess


def test_basic_cli():
    result = subprocess.run(['instld', os.path.join('tests', 'cli', 'quasi_empty_main.py')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))
    result.check_returncode()
