"""
mesclan.cache
~~~~~~~~~~~~~

Handlers redis caching
"""
from os import getenv
from redis import from_url

from mesclan.codec import dumps, loads
from mesclan.constants import REDIS_URL, REDIS_VAR
from mesclan.globals import redis


## Redis functions ##

def new_redis():
    """
    Get an instance of our redis connection
    """
    url = getenv(REDIS_VAR, REDIS_URL)
    return from_url(url)


def redis_set(id, data):
    """
    Set the bottle in redis data store
    """
    redis.set(id, dumps(data))


def redis_get(id):
    """
    Get a bottle's information from given its unique id
    """
    return loads(redis.get(id))
