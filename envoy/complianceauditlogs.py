"""
Resource that lists compliance audit logs for the Envoy node.
"""

from envoy.resource import Resource
from envoy.records import Record, PaginatedRecords
from envoy.exceptions import ReadOnlyEndpoint

class ComplianceAuditLog(Record):
    pass


class PaginatedComplianceAuditLogs(PaginatedRecords):

    CollectionKey = "logs"

    def cast(self, item):
        return ComplianceAuditLog(item)


class ComplianceAuditLogs(Resource):

    RecordType = ComplianceAuditLog
    RecordListType = PaginatedComplianceAuditLogs

    @property
    def endpoint(self):
        return "complianceauditlogs"

    def create(self) -> None:
        """ComplianceAuditLogs are a read-only resource; this function will raise envoy.exceptions.ReadOnlyEndpoint."""
        raise ReadOnlyEndpoint

    def update(self) -> None:
        """ComplianceAuditLogs are a read-only resource; this function will raise envoy.exceptions.ReadOnlyEndpoint."""
        raise ReadOnlyEndpoint

    def delete(self) -> None:
        """ComplianceAuditLogs are a read-only resource; this function will raise envoy.exceptions.ReadOnlyEndpoint."""
        raise ReadOnlyEndpoint
