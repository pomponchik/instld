import inspect

import pytest

from installed.errors import InstallingPackageError
from installed.cli.parsing_comments.get_comment_string import get_comment_string


def test_get_comment_started_with_instld():
    comment = get_comment_string(inspect.currentframe())  # instld: lol kek cheburek
    assert comment == 'lol kek cheburek'


def test_get_comment_not_started_with_instld():
    comment = get_comment_string(inspect.currentframe())  # lol kek cheburek
    assert comment is None


def test_get_comment_without_comment():
    comment = get_comment_string(inspect.currentframe())
    assert comment is None


def test_get_comment_wrong():
    with pytest.raises(InstallingPackageError):
        comment = get_comment_string(inspect.currentframe())  # instld:
