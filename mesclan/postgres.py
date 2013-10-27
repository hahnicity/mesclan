"""
mesclan.postgres
~~~~~~~~~~~~~~~~

As the name suggests handles all Postgres functions
"""
from contextlib import contextmanager
import csv
import logging
from os import listdir
from os.path import dirname, join
import re

from sqlalchemy.exc import IntegrityError

from mesclan import data
from mesclan.constants import DELIMITER
from mesclan.globals import postgresql
from mesclan.schema import Cellar


def add_and_commit(session, item):
    """
    Add an item to the postgres DB and then commit it
    """
    logging.debug("Add {} to the DB".format(item.__dict__))
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
        logging.warn("We were unable to load new data because there is existing data in the db")


def get_rows_by_total_views(limit):
    """
    Builds our initial cache in redis

    This is not a postgres function, but I'm trying to avoid import errors
    """
    with execute_session() as session:
        for obj in (session.query(Cellar).
                    order_by(Cellar.total_views.desc()).
                    limit(limit).all()):
            yield obj


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
        logging.info("Adding data from {} to the db".format(csv_file))
        with open(join(dirname(data.__file__), csv_file), "r") as csv_file:
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
            logging.debug("Adding id: {} name: {} to the DB".format(row[0], row[1]))
            add_and_commit(session, Cellar(id=row[0], name=row[1]))
