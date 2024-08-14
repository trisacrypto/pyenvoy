"""
Resource that manages the customer accounts the Envoy node knows about.
"""

from envoy.resource import Resource


class Accounts(Resource):

    @property
    def endpoint(self):
        return "accounts"
