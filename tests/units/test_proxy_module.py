import pytest

import installed


def test_convert_options():
    assert installed.convert_options({'platform': 'kek'}) == ['--platform', 'kek']
    assert installed.convert_options({'dry_run': True}) == ['--dry-run']
    assert installed.convert_options({'no_deps': False}) == []
    assert installed.convert_options({'platform': 'kek', 'dry_run': True}) == ['--platform', 'kek', '--dry-run']


def test_convert_options_wrong():
    with pytest.raises(ValueError):
        installed.convert_options({'kek': 'kek'})
    with pytest.raises(ValueError):
        installed.convert_options({'dry-run': 'kek'})
    with pytest.raises(ValueError):
        installed.convert_options({'--target': 'kek'})
    with pytest.raises(ValueError):
        installed.convert_options({'-t': 'kek'})
    with pytest.raises(ValueError):
        installed.convert_options({'--user': True})
    with pytest.raises(ValueError):
        installed.convert_options({'--root': 'kek'})
    with pytest.raises(ValueError):
        installed.convert_options({'platform': True})
    with pytest.raises(ValueError):
        installed.convert_options({'dry_run': 1})


def test_install_with_options():
    calls = []

    def runner(args, logger, catch_output, outputs):
        calls.append(args)

    with installed('kek_pack', runner=runner, platform='kek', no_deps=True):
        pass

    assert len(calls) == 1
    assert calls[0][4:] == ['--platform', 'kek', '--no-deps', 'kek_pack']
