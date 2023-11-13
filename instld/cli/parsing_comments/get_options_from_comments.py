from instld.errors import InstallingPackageError
from instld.cli.parsing_comments.get_comment_string import get_comment_string_by_frame


def get_options_from_comments(comment_string):
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

    result.pop('doc', None)
    result.pop('comment', None)

    return result

def get_options_from_comments_by_frame(frame):
    comment_string = get_comment_string_by_frame(frame)
    return get_options_from_comments(comment_string)
