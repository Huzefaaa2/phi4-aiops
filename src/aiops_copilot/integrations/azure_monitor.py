from __future__ import annotations

from datetime import timedelta
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus


class AzureMonitorIngestor:
    def __init__(self, workspace_id: str, tenant_id: str, client_id: str, client_secret: str) -> None:
        self.workspace_id = workspace_id
        credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        self.client = LogsQueryClient(credential)

    def get_windows_events(self, server_name: str, hours: int = 24) -> list[dict]:
        query = f"""
        Event
        | where TimeGenerated > ago({hours}h)
        | where Computer =~ '{server_name}'
        | project TimeGenerated, Computer, EventLevelName, EventID, Source, RenderedDescription
        | order by TimeGenerated desc
        """
        result = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
            timespan=timedelta(hours=hours),
        )
        if result.status != LogsQueryStatus.SUCCESS:
            return []
        table = result.tables[0]
        return [dict(zip(table.columns, row)) for row in table.rows]
