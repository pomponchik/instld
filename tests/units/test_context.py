from installed.context import Context


def test_context_repr():
    assert repr(Context('kek')) == 'Context("kek")'


def test_context_str():
    assert str(Context('kek')) == '<Context with path "kek">'
