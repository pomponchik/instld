from functools import lru_cache

from instld.errors import InstallingPackageError


@lru_cache()
def get_comment_string_from_file(line_number, file_name):
    try:
        with open(file_name, 'r') as file:
            for index, line in enumerate(file):
                if index + 1 == line_number:
                    splitted_line = line.split('#')
                    right_part = splitted_line[1:]
                    right_part = '#'.join(right_part)
                    right_part = right_part.strip()
                    if right_part.startswith('instld:'):
                        right_part = right_part[7:].strip()
                        if right_part:
                            return right_part
                        else:
                            raise InstallingPackageError('An empty list of options in the comment.')
                    break

    except (FileNotFoundError, OSError):
        return None

def get_comment_string(frame):
    line_number = frame.f_lineno
    code = frame.f_code
    file_name = code.co_filename

    return get_comment_string_from_file(line_number, file_name)
