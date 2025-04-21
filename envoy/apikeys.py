"""
Resource that manages the api keys that can access the Envoy node.
"""

from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords


class APIKey(Record):
    pass


class PaginatedAPIKeys(PaginatedRecords):

    CollectionKey = "api_keys"

    def cast(self, item):
        return APIKey(item)


class APIKeys(Resource):

    RecordType = APIKey
    RecordListType = PaginatedAPIKeys

    @property
    def endpoint(self):
        return "apikeys"
