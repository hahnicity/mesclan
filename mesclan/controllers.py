"""
mesclan.controllers
~~~~~~~~~~~~~~~~~
"""
from functools import wraps
import logging

from flask import request, Response
from sqlalchemy.orm.exc import NoResultFound
from ujson import dumps

from mesclan import exceptions
from mesclan.cache import build_cache
from mesclan.constants import DEBUG_TOKEN, GET_BOTTLE_FIELDS
from mesclan.handlers import handle_bottle_info


def handle_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            return Response(status=204)
        except exceptions.BAD_REQUEST_ERRORS as error:
            return dumps({"response": error.message}), 400
        except exceptions.InvalidTokenError as error:
            return dumps({"response": error.message}), 401
        except exceptions.CONFLICT_ERRORS as error:
            return dumps({"response": error.message}), 409
    return wrapper


def create_routes(app):
    @app.route("/bottle", methods=["POST"])
    @handle_request
    def get_bottle_info():
        """
        Get information for a bottle
        """
        logging.debug("A request was generated for bottle id: {}".format(request.form["id"]))
        _validate_fields(GET_BOTTLE_FIELDS)
        _validate_token()
        return handle_bottle_info(request.form["id"])

    @app.route("/trigger-task/update-cache", methods=["GET"])
    def update_cache():
        """
        Update our cache
        """
        logging.info("Updating the cache per request")
        build_cache()
        return Response(status=200)

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
