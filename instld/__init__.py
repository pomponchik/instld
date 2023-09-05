import sys

from installed.module.proxy_module import ProxyModule


sys.modules[__name__].__class__ = ProxyModule
