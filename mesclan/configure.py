"""
mesclan.configure
~~~~~~~~~~~~~~~
"""
from flask.ext.heroku import Heroku

from mesclan.constants import LOCAL_POSTGRES_URL
from mesclan.controllers import create_routes


def configure_app(app, args):
    """
    Configure the application's behavior
    """
    app.debug = args.debug
    app.testing = args.testing
    app.config["HOST"] = get_host(args)

    # Configure database
    configure_database(app)

    # Create all application controllers
    create_routes(app)


def configure_database(app):
    """
    If testing locally configure our db url
    """
    if app.debug or app.testing or app.config["HOST"] == "127.0.0.1":
        app.config["SQLALCHEMY_DATABASE_URI"] = LOCAL_POSTGRES_URL
    else:
        Heroku(app)


def get_host(args):
    """
    Configure the host string to run our app on
    """
    if args.host:
        return args.host
    else:
        return {True: "127.0.0.1", False: "0.0.0.0"}[args.local]
