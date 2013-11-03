"""
mesclan.builders
~~~~~~~~~~~~~~~~

Safe object building functions (Won't cause any collision with our globals)
for the SQLAlchemy db and Redis db
"""
from os import getenv

from redis import from_url
from flask.ext.sqlalchemy import SQLAlchemy

from mesclan.constants import REDIS_URL, REDIS_VAR


def new_postgresql(app):
    """
    Return our postgres database engine
    """
    return SQLAlchemy(app)


def new_redis():
    """
    Get an instance of our redis connection
    """
    url = getenv(REDIS_VAR, REDIS_URL)
    return from_url(url)
