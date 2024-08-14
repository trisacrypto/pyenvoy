"""
Resource that manages the counterparties the Envoy node knows about.
"""

from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords


class Counterparty(Record):
    pass


class PaginatedCounterparties(PaginatedRecords):

    CollectionKey = "counterparties"

    def cast(self, item):
        return Counterparty(item)


class Counterparties(Resource):

    RecordType = Counterparty
    RecordListType = PaginatedCounterparties

    @property
    def endpoint(self):
        return "counterparties"
