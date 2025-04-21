"""
Resource that manages the transactions the Envoy node is managing.
"""

from typing import TextIO

from envoy import client
from envoy.resource import Resource
from envoy.exceptions import ReadOnlyEndpoint
from envoy.records import Record, PaginatedRecords
from envoy.exceptions import AuthenticationError, ServerError, ClientError


CHUNK_SIZE = 1024 * 64


##########################################################################
## Data Records
##########################################################################


class Transaction(Record):

    def __init__(self, data=None, **kwargs):
        super(Transaction, self).__init__(data, **kwargs)
        self.secure_envelopes = SecureEnvelopes(self, self.parent.client)

    def send(self, envelope) -> dict:
        ep = self._make_endpoint("send")
        return Record(
            self.parent.client.post(envelope, *ep, require_authentication=True),
            parent=self,
        )

    def latest_payload(self, params=None) -> dict:
        ep = self._make_endpoint("payload")
        return Record(
            self.parent.client.get(*ep, params=params, require_authentication=True),
            parent=self,
        )

    def accept_preview(self, params=None) -> dict:
        ep = self._make_endpoint("accept")
        return Record(
            self.parent.client.get(*ep, params=params, require_authentication=True),
            parent=self,
        )

    def accept(self, envelope) -> dict:
        ep = self._make_endpoint("accept")
        return Record(
            self.parent.client.post(envelope, *ep, require_authentication=True),
            parent=self,
        )

    def reject(self, rejection) -> dict:
        ep = self._make_endpoint("reject")
        return Record(
            self.parent.client.post(rejection, *ep, require_authentication=True),
            parent=self,
        )

    def repair_preview(self, params=None) -> dict:
        ep = self._make_endpoint("repair")
        return Record(
            self.parent.client.get(*ep, params=params, require_authentication=True),
            parent=self,
        )

    def repair(self, envelope) -> dict:
        ep = self._make_endpoint("repair")
        return Record(
            self.parent.client.post(envelope, *ep, require_authentication=True),
            parent=self,
        )

    def archive(self) -> None:
        ep = self._make_endpoint("archive")
        self.parent.client.post(None, *ep, require_authentication=True)

    def unarchive(self) -> None:
        ep = self._make_endpoint("unarchive")
        self.parent.client.post(None, *ep, require_authentication=True)

    def _make_endpoint(self, *actions) -> tuple[str]:
        return tuple(["transactions", self["id"]] + list(actions))


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

    def prepare(self, prepare):
        return Record(
            self.client.post(
                prepare,
                *self._endpoint(),
                "prepare",
                require_authentication=True,
            ),
            parent=self,
        )

    def send_prepared(self, prepared):
        return Record(
            self.client.post(
                prepared,
                *self._endpoint(),
                "send-prepared",
                require_authentication=True,
            ),
            parent=self,
        )

    def export(self, f: TextIO, params: dict = None):
        """
        Export the transactions CSV file to the file-like object, f. This performs a
        streaming download of the possibly very large CSV file.

        Parameters
        ----------
        f : file-like object
            Either open a file on disk to write the file to or use the io package to
            collect the CSV data in memory. This object must have a write() method.

        params : dict, default None
            A dictionary of query parameters to attach to the URL.
        """
        self.client._pre_flight(require_authentication=True)
        uri = self.client._make_endpoint("transactions", "export")
        self.client._request_headers["Accept"] = "text/csv"

        kwargs = {
            "params": params,
            "headers": self.client._request_headers,
            "timeout": self.client.timeout,
            "stream": True,
        }

        # Perform a streaming download
        with self.client.session.get(uri, **kwargs) as reply:
            if reply.status_code != 200:
                if reply.status_code == 401 or reply.status_code == 403:
                    raise AuthenticationError("authentication failed")
                elif 400 <= reply.status_code < 500:
                    raise ClientError(reply.content)
                else:
                    raise ServerError(reply.content)

            content = reply.iter_content(chunk_size=CHUNK_SIZE, decode_unicode=True)
            for chunk in content:
                if chunk:
                    f.write(chunk)


class SecureEnvelopes(Resource):

    RecordType = SecureEnvelope
    RecordListType = PaginatedSecureEnvelopes

    def __init__(self, transaction: Transaction, client: "client.Client"):
        super(SecureEnvelopes, self).__init__(client)
        self.transaction = transaction

    @property
    def endpoint(self):
        return ("transactions", self.transaction["id"], "secure-envelopes")

    def create(self, data: dict, params: dict = None) -> dict:
        raise ReadOnlyEndpoint("transaction secure envelopes are a read-only endpoint")

    def update(self, data: dict, params: dict = None) -> dict:
        raise ReadOnlyEndpoint("transaction secure envelopes are a read-only endpoint")

    def delete(self, rid: str, params: dict = None) -> dict | None:
        raise ReadOnlyEndpoint("transaction secure envelopes are a read-only endpoint")
