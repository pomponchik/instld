import inspect

import pytest

from instld.errors import InstallingPackageError
from instld.cli.parsing_comments.get_options_from_comments import get_options_from_comments


def test_get_normal_options():
    options = get_options_from_comments(inspect.currentframe())  # instld: lol kek, cheburek mek

    assert isinstance(options, dict)
    assert len(options) == 2

    assert options['lol'] == 'kek'
    assert options['cheburek'] == 'mek'


def test_get_wrong_options():
    with pytest.raises(InstallingPackageError):
        options = get_options_from_comments(inspect.currentframe())  # instld: lol kek cheburek, cheburek mek
    with pytest.raises(InstallingPackageError):
        options = get_options_from_comments(inspect.currentframe())  # instld: lol
    with pytest.raises(InstallingPackageError):
        options = get_options_from_comments(inspect.currentframe())  # instld:


def test_get_empty_options():
    options = get_options_from_comments(inspect.currentframe())

    assert isinstance(options, dict)
    assert len(options) == 0
