"""
Exception class hierarchy for Envoy related exceptions.
"""


class EnvoyError(Exception):
    """
    Base class for all envoy related exceptions.
    """


class ServerError(EnvoyError):
    """
    An error that is raised when the server returns a 500 status code.
    """


class ClientError(EnvoyError):
    """
    An unspecified client side error when the server returns a 400 status code.
    """


class AuthenticationError(ClientError):
    """
    Occurs when the server returns a 401 or 403 error code.
    """


class NotFound(ClientError):
    """
    Occurs when the server returns a 404 error code.
    """


class ValidationError(ClientError):
    """
    The payload is invalid or a preflight check has failed.
    """


class ReadOnlyEndpoint(EnvoyError):
    """
    The associated resource does not allow create, update, or delete methods
    """
