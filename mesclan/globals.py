"""
mesclan.globals
~~~~~~~~~~~~~
"""
from peak.util.proxies import CallbackProxy
from mesclan.context import context

db = CallbackProxy(lambda: context["db"])
