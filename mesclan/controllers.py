"""
mesclan.controllers
~~~~~~~~~~~~~~~~~
"""
from functools import wraps

from flask import request
from ujson import dumps

from mesclan.constants import DEBUG_TOKEN, GET_BOTTLE_FIELDS
from mesclan import exceptions


def handle_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.BAD_REQUEST_ERRORS as error:
            return dumps({"response": error.message}), 400
        except exceptions.InvalidTokenError as error:
            return dumps({"response": error.message}), 401
        except exceptions.CONFLICT_ERRORS as error:
            return dumps({"response": error.message}), 409
    return wrapper


def create_routes(app):
    @app.route("/", methods=["POST"])
    @handle_request
    def get_bottle_info():
        """
        Handle login for customers to the app
        """
        _validate_fields(GET_BOTTLE_FIELDS)
        _validate_token()
        # RETURN some kind of translated redis obj

    def _validate_fields(fields):
        """
        Validate that correct parameters for a POST request were sent
        """
        for field in fields:
            if field not in request.form:
                raise exceptions.FieldNotFoundError(field)

    def _validate_token():
        """
        Validate the token we get from the mobile client
        """
        # XXX the DEBUG_TOKEN thing is only for dev purposes
        if request.form["token"] != DEBUG_TOKEN:
            raise exceptions.InvalidTokenError()
