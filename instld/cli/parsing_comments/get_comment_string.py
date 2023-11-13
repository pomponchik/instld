from functools import lru_cache

from instld.errors import InstallingPackageError
from instld.state_management.storage import state_storage, RunType


def get_comment_substring_from_string(string):
    splitted_line = string.split('#')
    right_part = splitted_line[1:]
    right_part = '#'.join(right_part)
    right_part = right_part.strip()
    if right_part.startswith('instld:'):
        right_part = right_part[7:].strip()
        if right_part:
            return right_part
        else:
            raise InstallingPackageError('An empty list of options in the comment.')

@lru_cache()
def get_comment_string_from_file(line_number, file_name):
    try:
        with open(file_name, 'r') as file:
            for index, line in enumerate(file):
                if index + 1 == line_number:
                    return get_comment_substring_from_string(line)

    except (FileNotFoundError, OSError):
        return None

def get_comment_string_by_frame(frame):
    if state_storage.run_type == RunType.script:
        line_number = frame.f_lineno
        code = frame.f_code
        file_name = code.co_filename

        return get_comment_string_from_file(line_number, file_name)

    elif state_storage.run_type == RunType.REPL:
        return get_comment_substring_from_string(state_storage.last_string)
