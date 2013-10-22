"""
mesclan.store
~~~~~~~~~~~~~

Handler for the data storage
"""
import os

from redis import from_url

from mesclan.codec import dumps, loads
from mesclan.constants import REDIS_URL, REDIS_VAR
from mesclan.globals import redis


def dump_bottle(id, data):
    """
    Set the bottle in data store
    """
    redis.set(id, dumps(data))


def get_redis():
    """
    Get an instance of our redis connection
    """
    url = os.getenv(REDIS_VAR, REDIS_URL)
    return from_url(url)


def get_bottle(id):
    """
    Get a bottle's information from given its unique id
    """
    return loads(redis.get(id))
