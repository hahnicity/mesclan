"""
mesclan.postgres
~~~~~~~~~~~~~~~~

As the name suggests handles all Postgres functions
"""
from contextlib import contextmanager
import csv
from os import listdir
from os.path import dirname, join
import re

from sqlalchemy.exc import IntegrityError

from mesclan import data
from mesclan.cache import redis_set
from mesclan.constants import (
    ARBITRARY_LIMIT, CACHE_BYTE_MARGIN, DELIMITER, MAX_CACHE_SPACE
)
from mesclan.globals import postgresql, redis
from mesclan.schema import Cellar


def add_and_commit(session, item):
    """
    Add an item to the postgres DB and then commit it
    """
    # XXX Log under info
    session.add(item)
    session.commit()


@contextmanager
def execute_session():
    """
    Execute some kind of action with a session object
    """
    try:
        yield postgresql.session
    except:
        postgresql.session.rollback()
        raise
    else:
        postgresql.session.commit()


def make_schema():
    """
    Initialize our postgres database
    """
    postgresql.create_all()
    try:
        load_data()
    except IntegrityError:
        # XXX Log as WARN!
        pass
    build_cache()


def build_cache():
    """
    Builds our initial cache in redis

    This is not a postgres function, but I'm trying to avoid import errors
    """
    def is_close_to_eom():
        # End of memory
        return redis.info()["used_memory"] + CACHE_BYTE_MARGIN >= MAX_CACHE_SPACE

    # Clear the cache first
    redis.flushdb()

    with execute_session() as session:
        items = iter(
            session.query(Cellar).
            order_by(Cellar.total_views.desc()).
            limit(ARBITRARY_LIMIT).all()
        )
        while not is_close_to_eom():
            try:
                to_add = sqla_obj_to_dict(items.next())
            except StopIteration:
                break
            else:
                # XXX Log as debug
                redis_set(to_add["id"], to_add)
        # XXX log finished with cache as debug


def sqla_obj_to_dict(obj):
    """
    Convert a SQLAlchemy row entry to a dictionary.

    Just using row.__dict__ is not sufficient for actually caching an object
    in redis. We must manually convert the row into a dictionary type
    """
    dict_ = dict(obj.__dict__)
    # SQLA has objects in __dict__ that are not actually columns, filter them
    del_keys = [key for key in dict_.iterkeys() if key.startswith("_")]
    for key in del_keys:
        del dict_[key]

    return dict_


def load_data():
    """
    Load all data in mesclan/data/*.csv into redis
    """
    csv_files = get_csv_files(dirname(data.__file__))
    for csv_file in csv_files:
        # XXX Log under debug
        with open(join(dirname(data.__file__), csv_file), "r") as csv_file:
            # XXX Log under debug
            translate_data(csv_file)


def get_csv_files(dir_):
    """
    Get all csv files in a directory
    """
    return [branch for branch in listdir(dir_) if re.search(".*csv", branch)]


def translate_data(csv_file):
    """
    Given an opened csv file, runs through each row and matches a row
    with the its corresponding data type.
    """
    reader = csv.reader(csv_file, delimiter=DELIMITER)
    with execute_session() as session:
        for row in reader:
            add_and_commit(session, Cellar(id=row[0], name=row[1]))
