import inspect

import pytest

from instld.errors import InstallingPackageError
from instld.cli.parsing_comments.get_options_from_comments import get_options_from_comments_by_frame


def test_get_normal_options():
    options = get_options_from_comments_by_frame(inspect.currentframe())  # instld: lol kek, cheburek mek

    assert isinstance(options, dict)
    assert len(options) == 2

    assert options['lol'] == 'kek'
    assert options['cheburek'] == 'mek'


# TODO: fix it!
@pytest.mark.skip("I'll fix it later.")
def test_real_options():
    options = get_options_from_comments_by_frame(inspect.currentframe())  # instld: where tests/cli/data/pok, version 1.0.4

    assert options == {
        'where': 'tests/cli/data/pok',
        'version': '1.0.4',
    }


def test_get_wrong_options():
    with pytest.raises(InstallingPackageError):
        get_options_from_comments_by_frame(inspect.currentframe())  # instld: lol kek cheburek, cheburek mek
    with pytest.raises(InstallingPackageError):
        get_options_from_comments_by_frame(inspect.currentframe())  # instld: lol
    with pytest.raises(InstallingPackageError):
        get_options_from_comments_by_frame(inspect.currentframe())  # instld:


def test_get_empty_options():
    options = get_options_from_comments_by_frame(inspect.currentframe())

    assert isinstance(options, dict)
    assert len(options) == 0
