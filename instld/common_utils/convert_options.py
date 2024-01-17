def convert_options(options):
    result = []

    def add_to_buffer(key, *value, is_option=True):
        if len(value) == 1:
            value = value[0]
        else:
            value = None

        string_variants = (
            '--requirement',
            '-r',
            '-c',
            '--constraint',
            '-e',
            '--editable',
            '-t',
            '--target',
            '--platform',
            '--python-version',
            '--implementation',
            '--abi',
            '--root',
            '--prefix',
            '--src',
            '--upgrade-strategy',
            '-C',
            '--config-settings',
            '--global-option',
            '--no-binary',
            '--only-binary',
            '--progress-bar',
            '--root-user-action',
            '--report',
            '-i',
            '--index-url',
            '--extra-index-url',
            '-f',
            '--find-links',
        )
        bool_variants = (
            '--no-deps',
            '--pre',
            '--dry-run',
            '--user',
            '-U',
            '--upgrade',
            '--force-reinstall',
            '-I',
            '--ignore-installed',
            '--ignore-requires-python',
            '--no-build-isolation',
            '--use-pep517',
            '--check-build-dependencies',
            '--break-system-packages',
            '--compile',
            '--no-compile',
            '--no-warn-script-location',
            '--no-warn-conflicts',
            '--prefer-binary',
            '--require-hashes',
            '--no-clean',
            '--no-index',
            '--isolated',
        )

        if key in string_variants:
            if not isinstance(value, str):
                raise ValueError(f'The "{key}" option must match a string value.')
        elif key in bool_variants:
            if value is not None:
                raise ValueError(f'The "{key}" option must match a bool value.')
        else:
            raise ValueError(
                f'Unknown option "{key}". Read the documentation: https://pip.pypa.io/en/stable/cli/pip_install/. '
                'If this option is present there, create an issue here: '
                'https://github.com/pomponchik/installed/issues/new'
            )

        if key in ('-t', '--target', '--user', '--root'):
            raise ValueError(f'The "{key}" option is incompatible with the library concept.')

        result.append(key)
        if value is not None:
            result.append(value)

    for name, value in options.items():
        name = name.replace('_', '-')

        if isinstance(value, str):
            if len(name) == 1:
                add_to_buffer(f'-{name}', value)
            else:
                add_to_buffer(f'--{name}', value)

        elif isinstance(value, bool):
            if value == True:
                if len(name) == 1:
                    add_to_buffer(f'-{name.upper()}')
                else:
                    add_to_buffer(f'--{name.lower()}')

        else:
            raise ValueError('The value must be a string or a boolean.')

    return result
