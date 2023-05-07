import pytest

from installed.utils.convert_options import convert_options


def test_convert_options():
    assert convert_options({'platform': 'kek'}) == ['--platform', 'kek']
    assert convert_options({'dry_run': True}) == ['--dry-run']
    assert convert_options({'no_deps': False}) == []
    assert convert_options({'platform': 'kek', 'dry_run': True}) == ['--platform', 'kek', '--dry-run']


def test_convert_options_wrong():
    with pytest.raises(ValueError):
        convert_options({'kek': 'kek'})
    with pytest.raises(ValueError):
        convert_options({'dry-run': 'kek'})
    with pytest.raises(ValueError):
        convert_options({'--target': 'kek'})
    with pytest.raises(ValueError):
        convert_options({'-t': 'kek'})
    with pytest.raises(ValueError):
        convert_options({'--user': True})
    with pytest.raises(ValueError):
        convert_options({'--root': 'kek'})
    with pytest.raises(ValueError):
        convert_options({'platform': True})
    with pytest.raises(ValueError):
        convert_options({'dry_run': 1})
