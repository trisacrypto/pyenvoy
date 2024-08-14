"""
Resource that manages the customer accounts the Envoy node knows about.
"""

from envoy import client
from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords


##########################################################################
## Data Records
##########################################################################


class Account(Record):

    def __init__(self, data=None, **kwargs):
        super(Account, self).__init__(data, **kwargs)
        self.crypto_addresses = CryptoAddresses(self, self.parent.client)


class PaginatedAccounts(PaginatedRecords):

    CollectionKey = "accounts"

    def cast(self, item):
        return Account(item, parent=self.parent)


class CryptoAddress(Record):
    pass


class PaginatedCryptoAddresses(PaginatedRecords):

    CollectionKey = "crypto_addresses"

    def cast(self, item):
        return CryptoAddress(item)


##########################################################################
## API Resources
##########################################################################

class Accounts(Resource):

    RecordType = Account
    RecordListType = PaginatedAccounts

    @property
    def endpoint(self):
        return "accounts"


class CryptoAddresses(Resource):

    RecordType = CryptoAddress
    RecordListType = PaginatedCryptoAddresses

    def __init__(self, account: Account, client: "client.Client"):
        super(CryptoAddresses, self).__init__(client)
        self.account = account

    @property
    def endpoint(self):
        return ("accounts", self.account["id"], "crypto-addresses")
