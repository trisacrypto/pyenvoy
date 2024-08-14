"""
Resource that manages the users that can access the Envoy node.
"""

from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords


class User(Record):
    pass


class PaginatedUsers(PaginatedRecords):

    CollectionKey = "users"

    def cast(self, item):
        return User(item)


class Users(Resource):

    RecordType = User
    RecordListType = PaginatedUsers

    @property
    def endpoint(self):
        return "users"
