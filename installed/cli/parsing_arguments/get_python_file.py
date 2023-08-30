import os
import sys


def get_python_file():
    if len(sys.argv) < 2:
        print('usage: instld python_file.py [argv ...]', file=sys.stderr, end=os.linesep)
        sys.exit(1)

    return sys.argv[1]
