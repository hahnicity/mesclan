"""
mesclan.globals
~~~~~~~~~~~~~
"""
from mesclan.context import get_global_object


redis = get_global_object("redis")
postgresql = get_global_object("postgresql")
