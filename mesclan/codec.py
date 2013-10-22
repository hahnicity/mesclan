"""
mesclan.codec
~~~~~~~~~~~~~
"""
import cPickle


def dumps(row):
    """
    Encode a csv row into a binary safe string
    """
    return cPickle.dumps(row)


def loads(data):
    """
    Loads a set of serialized data
    """
    return cPickle.loads(data)
