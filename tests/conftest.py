import os

import pytest
from termcolor import colored


@pytest.hookimpl
def pytest_runtest_makereport(item, call):
    """
    Хук, добавляющий информацию о текущих настройках к каждому выводу об ошибке в тесте.
    """
    if call.when == 'call':
        if call.excinfo:
            try:
                with open(os.path.join("tests", "cli", "data", "test.log"), 'r') as file:
                    text = file.read()
            except:
                text = 'NO DATA'
            item.add_report_section("call", "steps", colored(text, 'cyan'))
