import sys
import logging

from installed.context_manager import pip_context
from installed.runner import run_python
from installed.empty_logger import EmptyLogger


class ProxyModule(sys.modules[__name__].__class__):
    def __call__(self, *packages_names, logger=logging, runner=run_python):
        if logger is None:
            logger = EmptyLogger()
        return pip_context(packages_names, logger, runner)
