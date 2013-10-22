"""
mesclan.configure
~~~~~~~~~~~~~~~
"""
from mesclan.controllers import create_routes


def configure_app(app, args):
    """
    Configure the application's behavior
    """
    app.debug = args.debug
    app.testing = args.testing
    app.config["HOST"] = get_host(args)

    # Create all application controllers
    create_routes(app)


def get_host(args):
    """
    Configure the host string to run our app on
    """
    if args.host:
        return args.host
    else:
        return {True: "127.0.0.1", False: "0.0.0.0"}[args.local]
