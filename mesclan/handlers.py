"""
mesclan.handlers
~~~~~~~~~~~~~~~~

Handlers for the web to interact with the DB/Cache
"""
from ujson import dumps

from mesclan.cache import redis_get


def handle_bottle_info(id):
    """
    The request is in form of  flask.request

    Try to get data from cache first, if not available there search the DB.
    """
    # XXX Another avoidance of ImportErrors
    from mesclan.postgres import execute_session, sqla_obj_to_dict
    from mesclan.schema import Cellar

    try:
        bottle = dumps(redis_get(id))
        # XXX Log as debug
    except TypeError:  # cPickle will error out if it tries to decode None
        with execute_session() as session:
            bottle = dumps(sqla_obj_to_dict(Cellar.get_row_by_id(id, session)))
        # XXX Log as debug

    _update_total_views(id)
    return bottle


def _update_total_views(id):
    """
    Only update item in the DB, it doesn't actually matter whether we update
    the cache
    """
    # XXX I need to figure out a way not to do this
    from mesclan.postgres import execute_session
    from mesclan.schema import Cellar

    with execute_session() as session:
        Cellar.get_row_by_id(id, session).total_views += 1
