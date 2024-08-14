"""
Utilities endpoints provided as helpers by the Envoy node
"""

from envoy import client


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
            require_authentication=True
        )
        return reply["encoded"]

    def decode(self, travel_address: str) -> str:
        """
        Encodes a raw URI as a travel address.
        """
        data = {"encoded": travel_address}
        reply = self.client.post(
            data, "utilities", "travel-address", "decode", require_authentication=True
        )
        return reply["decoded"]
