"""
mesclan.handlers
~~~~~~~~~~~~~~~~

Handlers for the web to interact with the DB/Cache
"""
import logging

from ujson import dumps

from mesclan.cache import redis_get
from mesclan.postgres import execute_session, sqla_obj_to_dict
from mesclan.schema import Cellar


def handle_bottle_info(id):
    """
    The request is in form of  flask.request

    Try to get data from cache first, if not available there search the DB.
    """
    try:
        bottle = dumps(redis_get(id))
        logging.debug("item: {} was taken from the cache".format(bottle))
    except TypeError:  # cPickle will error out if it tries to decode None
        with execute_session() as session:
            bottle = dumps(sqla_obj_to_dict(Cellar.get_row_by_id(id, session)))
            logging.debug("item: {} was taken from the db".format(bottle))

    _update_total_views(id)
    return bottle


def _update_total_views(id):
    """
    Only update item in the DB, it doesn't actually matter whether we update
    the cache
    """
    with execute_session() as session:
        Cellar.get_row_by_id(id, session).total_views += 1
