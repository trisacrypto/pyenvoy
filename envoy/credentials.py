"""
Manages JWT credentials that are returned from the Envoy server on authentication.
"""

import jwt

from calendar import timegm
from datetime import datetime, timezone


class Credentials(object):
    """
    Credentials are composed of an access and a refresh token and are used to maintain
    authenticated state to the Envoy server. The credentials also contains other claims
    such as the permissions allowed by the specified API key.
    """

    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = Token(access_token)
        self.refresh_token = Token(refresh_token)

    def is_authenticated(self) -> bool:
        """
        Returns True if the access token is not expired
        """
        return not self.access_token.is_expired()

    def is_refreshable(self) -> bool:
        """
        Returns true if the refresh token is after the not before date and not expired.
        """
        return (
            not self.refresh_token.is_not_before()
            and not self.refresh_token.is_expired()
        )


class Token(object):
    """
    A token is a lightweight wrapper for JWT tokens and provides unverified decoding.
    """

    def __init__(self, token):
        self.token = token
        self._header = None
        self._claims = None

    def headers(self) -> dict:
        if self._header is None:
            self._header = jwt.get_unverified_header(self.token)
        return self._header

    def claims(self) -> dict:
        if self._claims is None:
            self._claims = jwt.decode(self.token, options={"verify_signature": False})
        return self._claims

    def is_expired(self) -> bool:
        """
        Returns true if the current time is after the exp claim.
        """
        exp = self.claims().get("exp", None)
        if exp is None:
            return True

        return timegm(datetime.now(tz=timezone.utc).utctimetuple()) > exp

    def is_not_before(self) -> bool:
        """
        Returns true if the current time is before the nbf claim.
        """
        nbf = self.claims().get("nbf", None)
        if nbf is None:
            return True

        return timegm(datetime.now(tz=timezone.utc).utctimetuple()) < nbf

    def __str__(self) -> str:
        return self.token
