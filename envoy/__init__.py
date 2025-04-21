"""
A Python API client for TRISA Envoy nodes. TRISA Envoy is an open source web service
that allows you to make travel rule information exchanges for compliance purposes using
both the TRISA and the TRP protocols. This Python library enables you to interact with
you deployed Envoy node.
"""

##########################################################################
## Module Info
##########################################################################

# Import the version number at the top level
from .version import get_version, __version_info__


##########################################################################
## Package Version
##########################################################################

__version__ = get_version(short=True)


##########################################################################
## Primary API entry point
##########################################################################

from dotenv import load_dotenv
from envoy.client import Client


def connect(url=None, client_id=None, client_secret=None, timeout=None):
    """
    Create an API client with the specified URL and api key material. If not specified,
    this function will first load any .env files in the local path, then attempt to
    configure the client from the environment.

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
    """

    if url is None or client_id is None or client_secret is None:
        # We need to load information from the environment
        load_dotenv()

    # create the client and perform the pre-flight now to authorize the client
    # now so the client's first actual data request isn't delayed by seconds
    client = Client(
        url=url, client_id=client_id, client_secret=client_secret, timeout=timeout
    )
    client._pre_flight(require_authentication=True)
    return client
