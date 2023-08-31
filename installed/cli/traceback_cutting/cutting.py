import io
import os
import sys
import traceback
from contextlib import redirect_stderr

from installed.cli.traceback_cutting.traceback_utils import cut_base_of_traceback


def create_cutting_excepthook(old_hook, base_size):
    def new_hook(exc_type, value, traceback_object):
        #traceback_object = cut_base_of_traceback(traceback_object, base_size)

        #buffer = io.StringIO()
        #with redirect_stderr(buffer):
        #    traceback.print_exception(exc_type, value, traceback_object)
        #traceback_string = buffer.getvalue()
        #if sys.platform.lower() in ('win32',):
        #    traceback_string = traceback_string.replace(os.linesep, '\n')
        #    traceback_string = traceback_string.replace('\n', os.linesep)


        #print(traceback_string, file=sys.stderr, end='')
        traceback.print_exception(exc_type, value, traceback_object)
    return new_hook


def set_cutting_excepthook(base_size):
    sys.excepthook = create_cutting_excepthook(sys.excepthook, base_size)
