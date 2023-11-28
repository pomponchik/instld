import sys
import traceback

from instld.cli.traceback_cutting.traceback_utils import cut_base_of_traceback, cut_importlib_bug


def create_cutting_excepthook(old_hook, base_size):
    def new_hook(exc_type, value, traceback_object):
        traceback_object = cut_base_of_traceback(traceback_object, base_size)
        traceback_object = cut_importlib_bug(traceback_object)
        traceback.print_exception(exc_type, value, traceback_object)
    return new_hook


def set_cutting_excepthook(base_size):
    sys.excepthook = create_cutting_excepthook(sys.excepthook, base_size)
