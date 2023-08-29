import os
import sys

import pytest


@pytest.fixture(scope='session')
def create_sitecustomize():
    with open(f'{sys.prefix}/lib/python3.9/site-packages/sitecustomize.py', 'w') as file:
        file.write('import coverage; import sys; coverage.process_startup(); open("/Users/evgeniy.blinov/Desktop/Projects/instld/file.txt", "a").write(f"{sys.prefix}\n")')
    with open(f'{sys.prefix}/lib/python3.9/site-packages/usercustomize.py', 'w') as file:
        file.write('import coverage; import sys; coverage.process_startup(); open("/Users/evgeniy.blinov/Desktop/Projects/instld/file.txt", "a").write(f"{sys.prefix}\n")')

    yield f'{sys.prefix}/lib/python3.9/site-packages/sitecustomize.py'
    os.remove(f'{sys.prefix}/lib/python3.9/site-packages/sitecustomize.py')


@pytest.fixture(scope='session')
def environment_with_coverage_on(create_sitecustomize):
    environ_copy = os.environ.copy()
    environ_copy.update({'INSTLD_COVERAGE_ON': 'True'})
    environ_copy.update({'COVERAGE_PROCESS_START': '.coveragerc'})
    environ_copy.update({'ENABLE_USER_SITE': 'True'})
    return environ_copy
