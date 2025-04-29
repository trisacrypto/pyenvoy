"""
Implements the API client that manages the authentication and cookie state of requests
to and from the Envoy server. This is a lower level object and should only be used by
advanced users.
"""

from __future__ import annotations

import os
import logging
import posixpath

from platform import python_version
from envoy.version import get_version

from requests import Response
from email.message import Message
from collections import namedtuple
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse, urlunparse, urlencode

from envoy.credentials import Credentials
from envoy.exceptions import AuthenticationError, ServerError, ClientError, NotFound

from envoy.accounts import Accounts
from envoy.transactions import Transactions
from envoy.counterparties import Counterparties
from envoy.users import Users
from envoy.apikeys import APIKeys
from envoy.utilities import Utilities

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


# Setup debug logging for pyenvoy
logger = logging.getLogger("envoy")


# Environment variables for local configuration
ENV_URL = "ENVOY_URL"
ENV_CLIENT_ID = "ENVOY_CLIENT_ID"
ENV_CLIENT_SECRET = "ENVOY_CLIENT_SECRET"

# Default header values
ACCEPT = "application/json"
ACCEPT_LANG = "en-US,en"
ACCEPT_ENCODE = "gzip, deflate, br"
CONTENT_TYPE = "application/json; charset=utf-8"


class Client(object):
    """
    Create a Client object to start making API calls to your Envoy API.

    Parameters
    ----------
    url : str
        The URL of your Envoy server (e.g. https://myenvoy.tr-envoy.com). If not
        set, it is discovered from the $ENVOY_URL environment variable.

    client_id : str
        The Client ID from your API Key to access your Envoy server. If not set, it
        is discovered from the $ENVOY_CLIENT_ID environment variable.

    client_secret : str
        The Client Secret from your API Key to access your Envoy server. If not set,
        it is discovered from the $ENVOY_CLIENT_SECRET environment variable.

    timeout : float
        The number of seconds to wait for a response until error.

    pool_connections : int
        The number of urllib3 connection pools to cache.

    pool_maxsize : int
        The maximum number of connections to save in the pool.

    max_retries : int
        The maximum number of retries each connection should attempt. Note, this
        applies only to failed DNS lookups, socket connections and connection
        timeouts, never to requests where data has made it to the server.
    """

    def __init__(
        self,
        url=None,
        client_id=None,
        client_secret=None,
        timeout=None,
        pool_connections=8,
        pool_maxsize=16,
        max_retries=3,
    ):
        self.client_id = client_id or os.environ.get(ENV_CLIENT_ID, None)
        self.client_secret = client_secret or os.environ.get(ENV_CLIENT_SECRET, None)

        url = url or os.environ.get(ENV_URL, "")

        self._creds = None
        self._host = parse_url_host(url)
        self._prefix = None

        user_agent = f"pyenvoy/{get_version(short=True)} python/{python_version()}"

        self.headers = {
            "User-Agent": user_agent,
            "Accept": ACCEPT,
            "Accept-Language": ACCEPT_LANG,
            "Accept-Encoding": ACCEPT_ENCODE,
            "Content-Type": CONTENT_TYPE,
        }

        # Configure HTTP requests with the requests library
        self.timeout = timeout
        self.session = Session()
        self.adapter = HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=max_retries,
        )
        self.session.mount(self.prefix + "://", self.adapter)

        # Configure REST resources on the client
        self.accounts = Accounts(self)
        self.transactions = Transactions(self)
        self.counterparties = Counterparties(self)
        self.users = Users(self)
        self.apikeys = APIKeys(self)
        self.utilities = Utilities(self)

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if value is None:
            self._timeout = (10.0, 30.0)
        else:
            self._timeout = value

    @property
    def prefix(self):
        if self._prefix is None:
            if not self._host:
                raise ValueError("cannot compute prefix without host")

            if self.is_localhost():
                self._prefix = "http"
            else:
                self._prefix = "https"

        return self._prefix

    @staticmethod
    def get_version(short: bool = None) -> str:
        """Returns the Client version."""
        if short is None:
            return get_version()
        else:
            return get_version(short)

    def status(self):
        return self.get("status", require_authentication=False)

    def get(
        self,
        *endpoint: tuple[str],
        params: dict = None,
        require_authentication: bool = True,
    ):
        self._pre_flight(require_authentication)
        headers = self._request_headers
        uri = self._make_endpoint(*endpoint)

        logger.debug(
            f"GET to {repr(uri)} with params {repr(params)} and headers {repr(headers)}"
        )

        rep = self.session.get(
            uri,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )

        return self.handle(rep)

    def post(
        self,
        data,
        *endpoint: tuple[str],
        params: dict = None,
        require_authentication: bool = True,
    ):
        self._pre_flight(require_authentication)
        headers = self._request_headers
        uri = self._make_endpoint(*endpoint)

        logger.debug(
            f"POST to {repr(uri)} with data {repr(data)} and headers {repr(headers)}"
        )

        rep = self.session.post(
            uri,
            json=data,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        return self.handle(rep)

    def put(
        self,
        data,
        *endpoint: tuple[str],
        params: dict = None,
        require_authentication: bool = True,
    ):
        self._pre_flight(require_authentication)
        headers = self._request_headers
        uri = self._make_endpoint(*endpoint)

        logger.debug(
            f"PUT to {repr(uri)} with data {repr(data)} and headers {repr(headers)}"
        )

        rep = self.session.put(
            uri,
            json=data,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        return self.handle(rep)

    def delete(
        self,
        *endpoint: tuple[str],
        params: dict = None,
        require_authentication: bool = True,
    ):
        self._pre_flight(require_authentication)
        headers = self._request_headers
        uri = self._make_endpoint(*endpoint)

        logger.debug(
            f"DELETE to {repr(uri)} with params {repr(params)} and headers {repr(headers)}"  # noqa
        )

        rep = self.session.delete(
            uri,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )

        return self.handle(rep)

    def handle(self, rep: Response):
        logger.debug(f"response headers {repr(rep.headers)}")

        # handle response based on status codes
        if rep.status_code == 401 or rep.status_code == 403:
            raise AuthenticationError("authentication failed")

        elif rep.status_code == 204:
            return None

        elif 200 <= rep.status_code < 300:
            mimetype, _ = parse_content_type(rep.headers.get("content-type"))
            if mimetype == "application/json":
                return rep.json()
            else:
                return rep.content

        elif 400 <= rep.status_code < 500:
            logger.warning(f"client error: {rep.status_code} {repr(rep.content)}")
            message = f"{rep.status_code} response from {self._host}]"

            try:
                err = rep.json()
                if "error" in err:
                    message = err["error"]
                if "errors" in err:
                    message += ":\n  " + "\n  ".join(
                        [f"{e['field']}: {e['error']}" for e in err["errors"]]
                    )
            except JSONDecodeError:
                pass

            if rep.status_code == 404:
                raise NotFound(message)
            else:
                raise ClientError(message)

        elif 500 <= rep.status_code < 600:
            logger.warning(f"server error: {rep.status_code} {repr(rep.content)}")
            message = f"{rep.status_code} response from {self._host}]"

            try:
                err = rep.json()
                if "error" in err:
                    message = err["error"]
            except JSONDecodeError:
                pass

            raise ServerError(message)

        else:
            raise ValueError(f"unhandled status code {rep.status_code}")

    def _make_endpoint(self, *endpoint: tuple[str], params: dict = None) -> str:
        """
        Creates an API endpoint from the specified resource endpoint, adding the api
        version identifier to the path to construct a valid Envoy URL.
        """
        path = posixpath.join("v1", *endpoint)
        params = params or {}

        return urlunparse(
            URL(
                scheme=self.prefix,
                netloc=self._host,
                path=path,
                params="",
                query=urlencode(params),
                fragment="",
            )
        )

    def _pre_flight(self, require_authentication: bool = True) -> None:
        if not self._host:
            raise ClientError("no envoy url or host specified")

        self._request_headers = {}
        self._request_headers.update(self.headers)

        if require_authentication:
            self._request_headers.update(self._authentication_headers())

    def _authentication_headers(self) -> dict:
        if not self.is_authenticated():
            # We need to reauthenticate, determine if we can refresh our credentials
            if self.is_refreshable():
                self._creds = self._reauthenticate()
            else:
                self._creds = self._authenticate()

        return {"Authorization": "Bearer " + str(self._creds.access_token)}

    def _authenticate(self) -> Credentials:
        if not self.client_id or not self.client_secret:
            raise AuthenticationError("no client id or secret specified")

        apikey = {"client_id": self.client_id, "client_secret": self.client_secret}
        rep = self.post(apikey, "authenticate", require_authentication=False)
        return Credentials(rep["access_token"], rep["refresh_token"])

    def _reauthenticate(self) -> Credentials:
        if not self._creds.refresh_token:
            raise AuthenticationError("no refresh token available")

        refresh = {"refresh_token": str(self._creds.refresh_token)}
        rep = self.post(refresh, "reauthenticate", require_authentication=False)
        return Credentials(rep["access_token"], rep["refresh_token"])

    def is_authenticated(self) -> bool:
        """
        Returns True if there are JWT claims with a valid access token
        """
        return self._creds is not None and self._creds.is_authenticated()

    def is_refreshable(self) -> bool:
        """
        Returns True if there are JWT claims with a valid refresh token
        """
        return self._creds is not None and self._creds.is_refreshable()

    def is_localhost(self) -> bool:
        """
        Returns true if the host is a local domain (e.g. localhost)
        """
        host = self._host
        if ":" in host:
            host = host.split(":")[0]
        return host == "localhost" or host.endswith(".local")


def parse_url_host(urlstr: str) -> str:
    parts = urlparse(urlstr, scheme="https", allow_fragments=False)
    if parts.netloc:
        return parts.netloc

    # if a domain is specified then it will be contained in the path
    return parts.path.split("/")[0]


def parse_content_type(mime: str) -> tuple[str, dict[str, str]]:
    msg = Message()
    msg["content-type"] = mime
    params = msg.get_params()
    return params[0][0], dict(params[1:])


URL = namedtuple(
    typename="URL",
    field_names=["scheme", "netloc", "path", "params", "query", "fragment"],
)
