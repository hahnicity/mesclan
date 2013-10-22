"""
mesclan.app
~~~~~~~~~~~~~~~~~
"""
from flask import Flask


def make_app():
    """
    Factory function for creating an app
    """
    return Flask(__name__)
