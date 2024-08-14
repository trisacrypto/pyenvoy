"""
Resource that manages the transactions the Envoy node is managing.
"""

from envoy.resource import Resource


class Transactions(Resource):

    @property
    def endpoint(self):
        return "transactions"
