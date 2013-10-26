"""
bamboo.schema.cellar
~~~~~~~~~~~~~~~~~~~~

The "liquor cellar" or where all records of our bottles are kept
"""
from mesclan.globals import postgresql as db


class Cellar(db.Model):
    __tablename__ = "cellar"

    # XXX These columns are pretty much debug until we get some real data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    total_views = db.Column(db.Integer)

    def __init__(self, id, name):
        self.id = int(id)  # Make sure this is an integer
        self.name = name
        self.total_views = 0

    @classmethod
    def get_row_by_id(cls, id, session):
        return session.query(cls).filter(cls.id == int(id)).one()
