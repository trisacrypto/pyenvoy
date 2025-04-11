"""
Resource that manages the customer accounts the Envoy node knows about.
"""

from envoy import client
from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords
from envoy.transactions import PaginatedTransactions
from envoy.exceptions import NotFound


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

    def lookup(self, crypto_address: str, params: dict = None) -> dict:
        """Lookup a customer account record by a crypto wallet address

        Args:
            crypto_address (str): the crypto wallet address to lookup the associated account for
            params (dict, optional): additional query parameters. Defaults to None.

        Raises:
            NotFound: when no account is found with a matching crypto address

        Returns:
            dict: an account
        """
        if params:
            params.update({"crypto_address": crypto_address})
        else:
            params = {"crypto_address": crypto_address}

        return self.RecordType(
            self.client.get(
                *self._endpoint(),
                "lookup",
                params=params,
                require_authentication=True,
            ),
            parent=self,
        )

    def transfers(self, rid: str, params: dict = None) -> list[dict]:
        """Search for all transfers related to the account by matching the associated crypto wallet addresses.

        Args:
            rid (str): the ID of the account to list transfers for
            params (dict, optional): additional query parameters. Defaults to None.

        Returns:
            list[dict]: a list of all transfers related to the account
        """
        return PaginatedTransactions(
            self.client.get(
                *self._endpoint(),
                rid,
                "transfers",
                params=params,
                require_authentication=True,
            ),
            parent=self,
        )

    def qrcode(self, rid: str, params: dict = None) -> bytes:
        """Returns the bytes for a QR code image for the account travel address.

        Args:
            rid (str): the ID of the account to get a QR code for
            params (dict, optional): additional query parameters. Defaults to None.

        Returns:
            bytes: image bytes that can be written directly to a file object
        """

        return self.client.get(
            *self._endpoint(),
            rid,
            "qrcode",
            params=params,
            require_authentication=True,
        )


class CryptoAddresses(Resource):

    RecordType = CryptoAddress
    RecordListType = PaginatedCryptoAddresses

    def __init__(self, account: Account, client: "client.Client"):
        super(CryptoAddresses, self).__init__(client)
        self.account = account

    @property
    def endpoint(self):
        return ("accounts", self.account["id"], "crypto-addresses")
