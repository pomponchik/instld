from installed.context import Context


def test_context_repr():
    assert repr(Context('kek', None)) == 'Context("kek")'


def test_context_str():
    assert str(Context('kek', None)) == '<Context with path "kek">'
