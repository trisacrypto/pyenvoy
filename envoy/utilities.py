"""
Utilities endpoints provided as helpers by the Envoy node
"""

from envoy import client


class Utilities(object):

    def __init__(self, client: "client.Client"):
        self.travel_addresses = TravelAddresses(client)
        self.ivms101_validator = IVMS101Validator(client)


class TravelAddresses(object):
    """
    Accesses the travel address encode and decode utilities on the Envoy node.
    """

    def __init__(self, client: "client.Client"):
        self.client = client

    def encode(self, rawuri: str) -> str:
        """
        Encodes a raw URI as a travel address.
        """
        data = {"decoded": rawuri}
        reply = self.client.post(
            data,
            "utilities",
            "travel-address",
            "encode",
            require_authentication=True,
        )
        return reply["encoded"]

    def decode(self, travel_address: str) -> str:
        """
        Encodes a raw URI as a travel address.
        """
        data = {"encoded": travel_address}
        reply = self.client.post(
            data,
            "utilities",
            "travel-address",
            "decode",
            require_authentication=True,
        )
        return reply["decoded"]


class IVMS101Validator(object):
    """
    Accesses the IVMS101 validator utility on the Envoy node.
    """

    def __init__(self, client: "client.Client"):
        self.client = client

    def validate(self, data: dict) -> dict:
        """Validates an arbitrary JSON payload as IVMS101 and returns the
        cross-protocol compatible JSON formatted IVMS101.

        Parameters
        ----------
        data : dict
            the IVMS101 object to validate

        Returns
        -------
        dict
            cross-protocol compatible IVMS101 object
        """

        return self.client.post(
            data,
            "utilities",
            "ivms101-validator",
            require_authentication=True,
        )
