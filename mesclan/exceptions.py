"""
mesclan.exceptions
~~~~~~~~~~~~~~~~~~~
"""


class FieldNotFoundError(Exception):
    def __init__(self, field):
        super(FieldNotFoundError, self).__init__(
            "The field {} was not found in your post!".format(field)
        )


class InvalidTokenError(Exception):
    def __init__(self):
        super(InvalidTokenError, self).__init__("You are not authorized to send requests")


class NoIDError(Exception):
    def __init__(self):
        super(NoIDError, self).__init__("No ID was specified")


class NoUserError(Exception):
    def __init__(self):
        super(NoUserError, self).__init__("No user was specified!")


class StatusCodeError(Exception):
    def __init__(self, response):
        msg = (
            "You received a non-200 status code: <{} code> because {}."
            " Your response was {}".format(
                response.status_code, response.reason, response.content
            )
        )
        super(StatusCodeError, self).__init__(msg)


BAD_REQUEST_ERRORS = (FieldNotFoundError, NoIDError, NoUserError)
CONFLICT_ERRORS = (StatusCodeError,)
