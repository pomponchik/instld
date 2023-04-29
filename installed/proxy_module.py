import sys

from installed.context_manager import pip_context


class ProxyModule(sys.modules[__name__].__class__):
    def __call__(self, *packages_names):
        return pip_context(*packages_names)
