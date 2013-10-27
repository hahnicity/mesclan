"""
mesclan.cache
~~~~~~~~~~~~~

Handlers for redis caching
"""
import logging

from mesclan.codec import dumps, loads
from mesclan.constants import ARBITRARY_LIMIT, CACHE_BYTE_MARGIN, MAX_CACHE_SPACE
from mesclan.globals import redis
from mesclan.postgres import get_rows_by_total_views, sqla_obj_to_dict


## Redis functions ##

def build_cache():
    """
    Rows should be an iterator of SQLA rows
    """
    def is_close_to_eom():
        # End of memory
        return redis.info()["used_memory"] + CACHE_BYTE_MARGIN >= MAX_CACHE_SPACE

    # Clear the cache first
    redis.flushdb()
    rows = get_rows_by_total_views(ARBITRARY_LIMIT)
    while not is_close_to_eom():
        try:
            to_add = sqla_obj_to_dict(rows.next())
        except StopIteration:
            break
        else:
            logging.debug("Add {} to the cache".format(to_add))
            redis_set(to_add["id"], to_add)
    logging.info("Finished adding rows to the cache")


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
