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
from mesclan.constants import ARBITRARY_LIMIT, CACHE_BYTE_MARGIN, DELIMITER, MAX_CACHE_SPACE
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

    if is_close_to_eom():
        # XXX log under info
        return

    with execute_session() as session:
        items = iter(session.query(Cellar).
                     order_by(Cellar.total_views).limit(ARBITRARY_LIMIT).all())
        while not is_close_to_eom():
            try:
                to_add = filter_for_valid_keys(items.next().__dict__)
            except StopIteration:
                break
            else:
                # XXX Log as debug
                redis_set(to_add["id"], to_add)


def filter_for_valid_keys(dict_):
    new_dict = dict(dict_)
    del_keys = [key for key in new_dict.iterkeys() if key.startswith("_")]
    for key in del_keys:
        del new_dict[key]

    return new_dict


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
    return [branch for branch in listdir(dir_) if re.findall(".*csv", branch)]


def translate_data(csv_file):
    """
    Given an opened csv file, runs through each row and matches a row
    with the its corresponding data type.
    """
    reader = csv.reader(csv_file, delimiter=DELIMITER)
    with execute_session() as session:
        for row in reader:
            add_and_commit(session, Cellar(id=row[0], name=row[1]))