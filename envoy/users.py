"""
Resource that manages the users that can access the Envoy node.
"""

from envoy.resource import Resource


class Users(Resource):

    @property
    def endpoint(self):
        return "users"
