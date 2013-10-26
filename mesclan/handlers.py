"""
mesclan.handlers
~~~~~~~~~~~~~~~~
"""
from ujson import dumps
from sqlalchemy.orm.exc import NoResultFound

from mesclan.cache import redis_get


def handle_bottle_info(id):
    """
    The request is in form of  flask.request

    Try to get data from cache first, if not available there search the DB.
    """
    # XXX Another avoidance of ImportErrors
    from mesclan.postgres import execute_session
    from mesclan.schema import Cellar
    try:
        print "BIN"
        print id
        print dumps(redis_get(id))
        return dumps(redis_get(id))
    except TypeError:  # cPickle will error out if it tries to decode None
        with execute_session() as session:
            return dumps(Cellar.get_row_by_id(id, session).__dict__)
    except NoResultFound:
        # XXX Throw an error
        pass
    except:
        # XXX do some kind of 404
        pass
