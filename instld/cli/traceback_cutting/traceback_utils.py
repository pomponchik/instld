def count_traceback_lenth(traceback_object):
    result = 0
    while traceback_object is not None:
        result += 1
        traceback_object = traceback_object.tb_next
    return result


def cut_base_of_traceback(traceback_object, base_size):
    index = 0
    while traceback_object is not None:
        #print(traceback_object.tb_frame.f_code.co_qualname, dir(traceback_object.tb_frame.f_code.co_qualname))
        if index == base_size:
            return traceback_object
        index += 1
        traceback_object = traceback_object.tb_next
