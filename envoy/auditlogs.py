"""
Resource that lists compliance audit logs for the Envoy node.
"""

from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords
from envoy.exceptions import ReadOnlyEndpoint


class AuditLog(Record):
    pass


class PaginatedAuditLogs(PaginatedRecords):

    CollectionKey = "logs"

    def cast(self, item):
        return AuditLog(item)


class AuditLogs(Resource):

    RecordType = AuditLog
    RecordListType = PaginatedAuditLogs

    @property
    def endpoint(self):
        return "auditlogs"

    def create(self) -> None:
        """Audit logs are a read-only resource; this function will raise envoy.exceptions.ReadOnlyEndpoint."""
        raise ReadOnlyEndpoint

    def update(self) -> None:
        """Audit logs are a read-only resource; this function will raise envoy.exceptions.ReadOnlyEndpoint."""
        raise ReadOnlyEndpoint

    def delete(self) -> None:
        """Audit logs are a read-only resource; this function will raise envoy.exceptions.ReadOnlyEndpoint."""
        raise ReadOnlyEndpoint
