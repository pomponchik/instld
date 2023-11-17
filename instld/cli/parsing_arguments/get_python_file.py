import sys


def get_python_file():
    if len(sys.argv) >= 2:
        return sys.argv[1]
