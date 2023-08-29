import io
import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from subprocess import CalledProcessError
from contextlib import redirect_stdout, redirect_stderr

import pytest

from installed.cli.main import start


@dataclass
class MainRunResult:
    stdout: bytes
    stderr: bytes
    returncode: int
    command: List[str]

    def check_returncode(self):
        if self.returncode != 0:
            raise CalledProcessError(self.returncode, self.command)

@pytest.fixture
def main_runner():
    def runner_function(arguments: List[str], env: Optional[Dict[str, str]] = None, **kwargs: Any):
        old_excepthook = sys.excepthook
        old_argv = sys.argv
        old_environ = os.environ
        old_exit = sys.exit

        if env is not None:
            os.environ = env

        sys.argv = arguments

        exits = []
        sys.exit = lambda x: exits.append(x)

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        returncode = 0
        with redirect_stdout(stdout_buffer) as stdout, redirect_stderr(stderr_buffer) as stderr:
            try:
                start()
            except Exception as e:
                returncode = 1
                sys.excepthook(type(e), e, e.__traceback__)
            finally:
                if len(exits) > 0:
                    returncode = 1
                result = MainRunResult(command=arguments, stdout=str.encode(stdout_buffer.getvalue()), stderr=str.encode(stderr_buffer.getvalue()), returncode=returncode)

        sys.excepthook = old_excepthook
        sys.argv = old_argv
        os.environ = old_environ
        sys.exit = old_exit

        return result

    yield runner_function
