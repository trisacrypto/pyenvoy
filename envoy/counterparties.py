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

    def search(self, query: str, limit: int = 10) -> Counterparty | PaginatedCounterparties: # noqa
        """
        Perform a fuzzy search of counterparty names that is case-insensitive, and
        normalizes unicode characters. The search results are ranked by match distance
        so the first results are more relevant than later results.

        Parameters
        ----------
        query : str
            The name of the counterparty you would like to search for.

        limit : int, default 10
            Limit the number of search results returned; for example to get only the
            first most relevant result, set the limit to 1.
        """
        params = {"query": query, "limit": limit}
        reply = self.client.get(
            self.endpoint, "search", params=params, require_authentication=True
        )

        if limit == 1 and len(reply["counterparties"]) == 1:
            return Counterparty(reply["counterparties"][0], parent=self)

        return PaginatedCounterparties(reply, parent=self)
