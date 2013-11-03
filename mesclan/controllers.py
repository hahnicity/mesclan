"""
mesclan.controllers
~~~~~~~~~~~~~~~~~
"""
from functools import wraps
from hashlib import sha256
import logging
from urlparse import urljoin

from flask import request, Response
import requests
from sqlalchemy.orm.exc import NoResultFound
from ujson import dumps

from mesclan import exceptions
from mesclan.cache import build_cache
from mesclan.constants import DEBUG_TOKEN, FACEBOOK_URL, GET_BOTTLE_FIELDS
from mesclan.handlers import handle_bottle_info


def handle_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.BAD_REQUEST_ERRORS as error:
            return dumps({"response": error.message}), 400
        except exceptions.InvalidTokenError as error:
            return dumps({"response": error.message}), 401
        except exceptions.UserUnderageError as error:
            return dumps({"response": error.message}), 404
        except NoResultFound:
            return Response(status=404)
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

    # XXX Trigger only with admin authentication
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

    def _validate_response(response):
        """
        Validate our response from the Facebook API
        """
        if response.status_code != 200:
            raise exceptions.StatusCodeError(response)
        else:
            return response

    def _validate_token():
        """
        Validate the token we get for requests to get information for a bottle
        """
        try:
            from mesclan import oauth
        except ImportError:
            _debug_flow()

        if app.debug or app.testing:
            _debug_flow()
        else:
            _facebook_flow(oauth)

    def _debug_flow():
        """
        Run through the debug flow for validating a user's token
        """
        if request.form["token"] != DEBUG_TOKEN:
            raise exceptions.InvalidTokenError()

    def _facebook_flow(oauth):
        """
        Run through the actual facebook flow for validating a user's token.

        1. Construct a hash of the appsecret_proof
        2. Call the facebook Graph API, validate the age range
        """
        appsecret_proof = sha256()
        appsecret_proof.update(request.form["token"])
        appsecret_proof.update(oauth.SECRET)
        hash_ = appsecret_proof.digest()
        response = _validate_response(requests.get(
            "{}/age_range?access_token={}".format(
                urljoin(FACEBOOK_URL, request.form["user_id"]), request.form["token"]
            ),
            headers={"appsecret_proof", hash_}
        ))
        # validate age, must be 21 in USA. Because we are making a liquor app...
        if response.json()["min"] != "21":
            raise exceptions.UserUnderageError()
