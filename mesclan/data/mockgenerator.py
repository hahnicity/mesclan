"""
mesclan.data.mockgenerator
~~~~~~~~~~~~~~~~~~~~~~~~~~

A program to generate mock csv data in lieu of not actually having anything
"""
from random import choice
from string import ascii_uppercase, digits


def generate_string(n):
    """
    Generate a random string of random uppercase letters and digits
    """
    return ''.join(choice(ascii_uppercase + digits) for x in xrange(n))


def generate_csv(rows, columns, entry_length):
    """
    Generate a csv document with rows and columns of mock data
    """
    with open("mockdata.csv", "w") as file_:
        # Write field types, 10 is arbitrary
        file_.write("{}\n".format(",".join(
            ["id"] + [generate_string(10) for _ in xrange(columns - 1)])
        ))
        for number in xrange(rows):
            line = ",".join(
                [str(number)] +
                [generate_string(entry_length) for _ in xrange(columns - 1)]
            )
            file_.write("{}\n".format(line))
