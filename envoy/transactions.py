"""
Resource that manages the transactions the Envoy node is managing.
"""

from envoy import client
from envoy.resource import Resource
from envoy.exceptions import ReadOnlyEndpoint
from envoy.records import Record, PaginatedRecords


##########################################################################
## Data Records
##########################################################################

class Transaction(Record):

    def __init__(self, data=None, **kwargs):
        super(Transaction, self).__init__(data, **kwargs)
        self.secure_envelopes = SecureEnvelopes(self, self.parent.client)


class PaginatedTransactions(PaginatedRecords):

    CollectionKey = "transactions"

    def cast(self, item):
        return Transaction(item, parent=self.parent)


class SecureEnvelope(Record):
    pass


class PaginatedSecureEnvelopes(PaginatedRecords):

    def cast(self, item):
        return SecureEnvelope(item)

    def _collection_key(self, data):
        if "is_decrypted" in data:
            if data["is_decrypted"]:
                return "envelopes"
            else:
                return "secure_envelopes"
        return super(PaginatedSecureEnvelopes, self)._collection_key(data)


##########################################################################
## API Resources
##########################################################################

class Transactions(Resource):

    RecordType = Transaction
    RecordListType = PaginatedTransactions

    @property
    def endpoint(self):
        return "transactions"


class SecureEnvelopes(Resource):

    RecordType = SecureEnvelope
    RecordListType = PaginatedSecureEnvelopes

    def __init__(self, transaction: Transaction, client: "client.Client"):
        super(SecureEnvelopes, self).__init__(client)
        self.transaction = transaction

    @property
    def endpoint(self):
        return ("transactions", self.transaction["id"], "secure-envelopes")

    def create(self, data: dict) -> dict:
        raise ReadOnlyEndpoint("transaction secure envelopes are a read-only endpoint")

    def update(self, data: dict) -> dict:
        raise ReadOnlyEndpoint("transaction secure envelopes are a read-only endpoint")

    def delete(self, rid: str, params: dict = None) -> dict | None:
        raise ReadOnlyEndpoint("transaction secure envelopes are a read-only endpoint")
