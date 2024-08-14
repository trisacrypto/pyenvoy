"""
Resource that manages the customer accounts the Envoy node knows about.
"""

from envoy import client
from envoy.resource import Resource


class Accounts(Resource):

    @property
    def endpoint(self):
        return "accounts"


class CryptoAddresses(Resource):

    def __init__(self, accountID: str, client: "client.Client"):
        super(CryptoAddresses, self).__init__(client)
        self.accountID = accountID

    @property
    def endpoint(self):
        return ("accounts", self.accountID, "crypto-addresses")
