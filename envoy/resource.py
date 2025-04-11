"""
A resource is a base class that provides standard REST functionality to an API resource
serviced by the API. The basic functionality is list, create, detail, update, and
delete. Most interactions with the Envoy API are via a resource object.
"""

from envoy import client
from envoy.exceptions import ValidationError
from envoy.records import Record, PaginatedRecords


class Resource(object):
    """
    Resource objects are not intended to be used directly but are intended to be
    subclassed by resources to provide the standard functionality for REST operations.
    """

    RecordType = Record
    RecordListType = PaginatedRecords

    def __init__(self, client: "client.Client"):
        self.client = client

    @property
    def endpoint(self):
        raise AttributeError("subclasses should define the endpoint for their resource")

    def list(self, params: dict = None) -> list[dict]:
        return self.RecordListType(
            self.client.get(
                *self._endpoint(),
                params=params,
                require_authentication=True,
            ),
            parent=self,
        )

    def create(self, data: dict, params: dict = None) -> dict:
        return self.RecordType(
            self.client.post(
                data,
                *self._endpoint(),
                params=params,
                require_authentication=True,
            ),
            parent=self,
        )

    def detail(self, rid: str, params: dict = None) -> dict:
        return self.RecordType(
            self.client.get(
                *self._endpoint(),
                rid,
                params=params,
                require_authentication=True,
            ),
            parent=self,
        )

    def update(self, data: dict, params: dict = None) -> dict:
        if "id" not in data:
            raise ValidationError("an ID is required to update this resource")

        return self.RecordType(
            self.client.put(
                data,
                *self._endpoint(),
                data["id"],
                params=params,
                require_authentication=True,
            ),
            parent=self,
        )

    def delete(self, rid: str, params: dict = None) -> dict | None:
        return self.client.delete(
            *self._endpoint(),
            rid,
            params=params,
            require_authentication=True,
        )

    def _endpoint(self):
        endpoint = self.endpoint
        if isinstance(endpoint, str):
            return (endpoint,)
        return endpoint
