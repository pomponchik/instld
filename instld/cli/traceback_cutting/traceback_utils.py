def count_traceback_lenth(traceback_object):
    result = 0
    while traceback_object is not None:
        result += 1
        traceback_object = traceback_object.tb_next
    return result


def cut_base_of_traceback(traceback_object, base_size):
    index = 0
    while traceback_object is not None:
        if index == base_size:
            return traceback_object
        index += 1
        traceback_object = traceback_object.tb_next


def cut_importlib_bug(traceback_object):
    """
    This function fix the truble, that occurs only for windows.

    See: https://github.com/pomponchik/instld/actions/runs/6997770395
    """
    try:
        while traceback_object is not None:
            if not (traceback_object.tb_frame.f_code.co_filename == '<frozen importlib._bootstrap>' or traceback_object.tb_frame.f_code.co_filename == '<frozen importlib._bootstrap_external>'):
                return traceback_object
            traceback_object = traceback_object.tb_next
    except AttributeError:
        return traceback_object
