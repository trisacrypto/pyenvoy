"""
Resource that manages the api keys that can access the Envoy node.
"""

from envoy.resource import Resource


class APIKeys(Resource):

    @property
    def endpoint(self):
        return "apikeys"
