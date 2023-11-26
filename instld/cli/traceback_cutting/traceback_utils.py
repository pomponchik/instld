def count_traceback_lenth(traceback_object):
    result = 0
    while traceback_object is not None:
        result += 1
        traceback_object = traceback_object.tb_next
    return result


def cut_base_of_traceback(traceback_object, base_size):
    index = 0
    while traceback_object is not None:
        #print(traceback_object.tb_frame.f_code.co_qualname, traceback_object.tb_frame.f_code.co_filename)
        if index == base_size:
            return traceback_object
        index += 1
        traceback_object = traceback_object.tb_next


def cut_importlib_bug(traceback_object):
    try:
        while traceback_object is not None:
            if not (traceback_object.tb_frame.f_code.co_qualname == '_call_with_frames_removed' and traceback_object.tb_frame.f_code.co_filename == '<frozen importlib._bootstrap>'):
                return traceback_object
            traceback_object = traceback_object.tb_next
    except AttributeError:
        return traceback_object
