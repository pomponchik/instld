from instld.module.context import Context


def test_context_repr():
    assert repr(Context('kek', None, None, None, None)) == 'Context("kek")'


def test_context_str():
    assert str(Context('kek', None, None, None, None)) == '<Context with path "kek">'
