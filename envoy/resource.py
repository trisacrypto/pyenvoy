"""
A resource is a base class that provides standard REST functionality to an API resource
serviced by the API. The basic functionality is list, create, detail, update, and
delete. Most interactions with the Envoy API are via a resource object.
"""

from envoy import client
from envoy.exceptions import ValidationError


class Resource(object):
    """
    Resource objects are not intended to be used directly but are intended to be
    subclassed by resources to provide the standard functionality for REST operations.
    """

    def __init__(self, client : "client.Client"):
        self.client = client

    @property
    def endpoint(self):
        raise AttributeError("subclasses should define the endpoint for their resource")

    def list(self, params: dict = None) -> list[dict]:
        return self.client.get(
            self.endpoint, params=params, require_authentication=True
        )

    def create(self, data: dict) -> dict:
        return self.client.post(
            data, self.endpoint, require_authentication=True
        )

    def detail(self, rid: str, params: dict = None) -> dict:
        return self.client.get(
            self.endpoint, rid, params=params, require_authentication=True
        )

    def update(self, data: dict) -> dict:
        if "id" not in data:
            raise ValidationError("an ID is required to update this resource")

        return self.client.put(
            data, self.endpoint, data["id"], require_authentication=True
        )

    def delete(self, rid: str, params: dict = None) -> dict | None:
        return self.client.delete(
            self.endpoint, rid, params=params, require_authentication=True
        )
