"""
mesclan.store
~~~~~~~~~~~~~

Handler for the data storage
"""
import csv
from os import getenv, listdir
from os.path import dirname, join

from redis import from_url

from mesclan import data
from mesclan.codec import dumps, loads
from mesclan.constants import DELIMITER, REDIS_URL, REDIS_VAR
from mesclan.globals import redis


def dump_bottle(id, data):
    """
    Set the bottle in data store
    """
    redis.set(id, dumps(data))


def get_redis():
    """
    Get an instance of our redis connection
    """
    url = getenv(REDIS_VAR, REDIS_URL)
    return from_url(url)


def get_bottle(id):
    """
    Get a bottle's information from given its unique id
    """
    return loads(redis.get(id))


def get_csv_files(dir_):
    """
    Get all csv files in a directory
    """
    return [
        join(dir_, branch) for branch in listdir(dir_)
        if branch.split(".")[-1] == "csv"
    ]


def load_data():
    """
    Load all data in mesclan/data/*.csv into redis
    """
    csv_files = get_csv_files(dirname(data.__file__))
    # XXX This gets pretty speculative in terms of what the structure
    # of the data will look like. Is def. DEBUG
    for file_ in csv_files:
        with open(file_, "r") as csv_file:
            translate_data(csv_file)


def translate_data(csv_file):
    """
    Given an opened csv file, runs through each row and matches a row
    with the its corresponding data type.
    """
    reader = csv.reader(csv_file, delimiter=DELIMITER)
    fields = reader.next()  # Get the first row where the fields are delineated
    for row in reader:
        data = {fields[i]: row[i] for i in xrange(len(row))}
        dump_bottle(data["id"], data)
