"""
mesclan.main
~~~~~~~~~~
"""
from argparse import ArgumentParser
from os import environ

from mesclan.app import make_app
from mesclan.configure import configure_app
from mesclan.context import mesclan_context
from mesclan.store import get_redis


def build_parser():
    """
    #Parse all command line arguments
    """
    parser = ArgumentParser()
    add_app_arguments(parser)
    add_other_arguments(parser)
    return parser


def add_app_arguments(parser):
    """
    #Add arguments for where the app will be run
    """
    hosts = parser.add_mutually_exclusive_group()
    hosts.add_argument("--local", help="Launch the app on 127.0.0.1", action="store_true")
    hosts.add_argument("--host", help="Launch the app on a specific host eg: 1.1.1.1")


def add_other_arguments(parser):
    """
    #Add other arguments
    """
    others = parser.add_argument_group("Other Options")
    others.add_argument(
        "--debug",
        help="Enable exception logging and reload the app if the source changes",
        action="store_true",
    )
    others.add_argument(
        "--testing",
        help="Enable exception logging and usage of mocks for configuration functions",
        action="store_true",
    )


def main():
    """
    Console Entry point
    """
    app = make_app()
    with mesclan_context(redis=get_redis()):
        args = build_parser().parse_args()
        configure_app(app, args)
        app.run(host=app.config["HOST"], port=int(environ.get("PORT", 5000)))



if __name__ == "__main__":
    main()
