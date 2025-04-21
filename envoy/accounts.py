"""
Resource that manages the customer accounts the Envoy node knows about.
"""

from io import BytesIO

from envoy import client
from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords
from envoy.transactions import PaginatedTransactions


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

        Parameters
        ----------
        crypto_address : str
            the crypto wallet address to lookup the associated account for
        params : dict, optional
            additional query parameters, by default None

        Returns
        -------
        dict
            an account
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
        """Search for all transfers related to the account by matching the associated
        crypto wallet addresses.

        Parameters
        ----------
        rid : str
            the ID of the account to list transfers for
        params : dict, optional
            additional query parameters, by default None

        Returns
        -------
        list[dict]
            a list of all transfers related to the account
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

    def qrcode(self, rid: str) -> BytesIO:
        """Generate and download a QR code for the account travel address.

        Parameters
        ----------
        rid : str
            the ID of the crypto address to generate a QR code for

        Returns
        -------
        BytesIO
            the QR code image bytes
        """

        return BytesIO(
            self.client.get(
                *self._endpoint(),
                rid,
                "qrcode",
                require_authentication=True,
            )
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

    def qrcode(self, rid: str) -> BytesIO:
        """Generate and download a QR code for the travel address associated with the
        crypto wallet address.

        Parameters
        ----------
        rid : str
            the ID of the crypto address to generate a QR code for

        Returns
        -------
        BytesIO
            the QR code image bytes
        """

        return BytesIO(
            self.client.get(
                *self._endpoint(),
                rid,
                "qrcode",
                require_authentication=True,
            )
        )
