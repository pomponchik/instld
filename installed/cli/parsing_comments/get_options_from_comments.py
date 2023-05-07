from installed.errors import InstallingPackageError
from installed.cli.parsing_comments.get_comment_string import get_comment_string


def get_options_from_comments(frame):
    frame = frame.f_back
    comment_string = get_comment_string(frame)

    result = {}

    if comment_string is not None:
        options = (x.strip() for x in comment_string.split(','))
        options = (x for x in options if x)

        for option in options:
            splitted_option = [x for x in option.split() if x]

            if len(splitted_option) != 2:
                raise InstallingPackageError('Incorrect comment format.')

            option_name = splitted_option[0].strip().lower()
            option_value = splitted_option[1].strip().lower()
            result[option_name] = option_value

    return result
