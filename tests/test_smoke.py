import importlib

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
