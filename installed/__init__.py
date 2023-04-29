import sys

from installed.proxy_module import ProxyModule


sys.modules[__name__].__class__ = ProxyModule
