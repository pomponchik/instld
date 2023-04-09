import sys

import installed
import copy


def test_sys_path_lenth():
    number_before = len(sys.path)
    sys_path_copy = copy.copy(sys.path)

    with installed('polog'):
        assert len(sys.path) == number_before + 1
        assert sys.path[1:] == sys_path_copy

    assert len(sys.path) == number_before
