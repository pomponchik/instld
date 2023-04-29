import sys
import importlib
import copy

import pytest

import installed


def test_polog_install_and_import():
    with installed('polog'):
        from polog import log, config, file_writer


def test_polog_install_two_and_import():
    with installed('polog', 'astrologic'):
        from polog import log, config, file_writer
        from astrologic import switcher


def test_polog_install_two_contexts_and_import():
    with installed('polog'):
        with installed('astrologic'):
            from polog import log, config, file_writer
            from astrologic import switcher


def test_deleting_contexts():
    with installed('polog'):
        with installed('astrologic'):
            pass
    with pytest.raises(ModuleNotFoundError):
        import polog
        importlib.reload(polog)




def test_sys_path_lenth():
    number_before = len(sys.path)
    sys_path_copy = copy.copy(sys.path)

    with installed('polog'):
        assert len(sys.path) == number_before + 1
        assert sys.path[1:] == sys_path_copy

    assert len(sys.path) == number_before
