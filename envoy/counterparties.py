"""
Resource that manages the counterparties the Envoy node knows about.
"""

from envoy.resource import Resource


class Counterparties(Resource):

    @property
    def endpoint(self):
        return "counterparties"
