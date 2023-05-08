import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='Running a script with automatic installation of dependencies.')
    parser.add_argument('python_file', type=str, help='The path to the file with the extension ".py" containing Python code.')
    arguments = parser.parse_args()

    return arguments
