import inspect

import pytest

from instld.errors import InstallingPackageError
from instld.cli.parsing_comments.get_comment_string import get_comment_string_by_frame, get_comment_substring_from_string


def test_get_comment_started_with_instld():
    comment = get_comment_string_by_frame(inspect.currentframe())  # instld: lol kek cheburek
    assert comment == 'lol kek cheburek'


def test_get_comment_not_started_with_instld():
    comment = get_comment_string_by_frame(inspect.currentframe())  # lol kek cheburek
    assert comment is None


def test_get_comment_without_comment():
    comment = get_comment_string_by_frame(inspect.currentframe())
    assert comment is None


def test_get_comment_wrong():
    with pytest.raises(InstallingPackageError):
        comment = get_comment_string_by_frame(inspect.currentframe())  # instld:


def test_get_comment_substring_from_string():
    assert get_comment_substring_from_string('a + b # kek') is None
    assert get_comment_substring_from_string('a + b # instld: lol kek') == 'lol kek'

    with pytest.raises(InstallingPackageError):
        assert get_comment_substring_from_string('a + b # instld: ')
