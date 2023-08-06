import installed


def test_install_with_options():
    calls = []

    def runner(args, logger, catch_output):
        calls.append(args)

    with installed('kek_pack', runner=runner, platform='kek', no_deps=True):
        pass

    assert len(calls) == 1
    assert calls[0][4:] == ['--platform', 'kek', '--no-deps', 'kek_pack']
