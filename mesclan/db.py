"""
mesclan.db
~~~~~~~~~~
"""
from flask.ext.sqlalchemy import SQLAlchemy


def make_postgresql(app):
    """
    Return our postgres database engine
    """
    return SQLAlchemy(app)
