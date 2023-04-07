import installed


def test_polog_install_and_import():
    with installed('polog'):
        from polog import log, config, file_writer
