"""Power BI REST API Client for DataTrace.

Provides comprehensive Power BI REST API integration.
"""

import logging
from typing import Optional, Any

import requests

from datatrace.config.settings import get_settings
from datatrace.lib.auth.powerbi import ServicePrincipalAuth, UserAuth
from datatrace.lib.exceptions import (
    ConnectionError,
    DiscoveryError,
    AuthenticationError,
    RateLimitError,
)

logger = logging.getLogger(__name__)

# Power BI REST API base URL
POWERBI_API_BASE = "https://api.powerbi.com/v1.0/myorg"


class PowerBIClient:
    """Power BI REST API client.

    Provides methods to interact with Power BI REST API for metadata extraction.
    """

    def __init__(
        self,
        auth: Optional[ServicePrincipalAuth | UserAuth] = None,
        workspace_id: Optional[str] = None,
    ):
        """Initialize Power BI client.

        Args:
            auth: Authentication handler (ServicePrincipalAuth or UserAuth)
            workspace_id: Optional default workspace ID
        """
        self.settings = get_settings().powerbi
        self.auth = auth or ServicePrincipalAuth()
        self.workspace_id = workspace_id
        self._access_token: Optional[str] = None

    @property
    def access_token(self) -> str:
        """Get or refresh access token."""
        if self._access_token is None:
            self._access_token = self.auth.get_access_token()
        return self._access_token

    @property
    def headers(self) -> dict[str, str]:
        """Get HTTP headers for API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        """Make HTTP request to Power BI API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path (without base URL)
            params: Query parameters
            data: Form data
            json: JSON data

        Returns:
            Response JSON data
        """
        url = f"{POWERBI_API_BASE}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                data=data,
                json=json,
                timeout=30,
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise RateLimitError(
                    f"Power BI API rate limit exceeded. Retry after {retry_after} seconds.",
                    retry_after=retry_after,
                )

            # Handle authentication errors
            if response.status_code == 401 or response.status_code == 403:
                # Try refreshing token
                self._access_token = None
                self._access_token = self.auth.get_access_token()
                # Retry once
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    data=data,
                    json=json,
                    timeout=30,
                )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Power BI API request failed: {method} {url} - {e}")
            raise ConnectionError(f"Power BI API request failed: {e}", connection_type="powerbi")

    def get_workspaces(self) -> list[dict[str, Any]]:
        """Get all Power BI workspaces.

        Returns:
            List of workspace dictionaries
        """
        result = self._make_request("GET", "/groups")
        workspaces = result.get("value", [])
        logger.info(f"Found {len(workspaces)} Power BI workspaces")
        return workspaces

    def get_datasets(self, workspace_id: Optional[str] = None) -> list[dict[str, Any]]:
        """Get all datasets in a workspace.

        Args:
            workspace_id: Workspace ID. If None, uses default workspace

        Returns:
            List of dataset dictionaries
        """
        wid = workspace_id or self.workspace_id
        if not wid:
            raise DiscoveryError(
                "workspace_id is required for get_datasets",
                resource_type="powerbi_dataset",
            )
        result = self._make_request("GET", f"/groups/{wid}/datasets")
        datasets = result.get("value", [])
        logger.info(f"Found {len(datasets)} datasets in workspace {wid}")
        return datasets

    def get_dataset(self, workspace_id: str, dataset_id: str) -> dict[str, Any]:
        """Get a specific dataset.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID

        Returns:
            Dataset dictionary
        """
        result = self._make_request("GET", f"/groups/{workspace_id}/datasets/{dataset_id}")
        logger.debug(f"Retrieved dataset {dataset_id} from workspace {workspace_id}")
        return result

    def get_tables(self, workspace_id: str, dataset_id: str) -> list[dict[str, Any]]:
        """Get all tables in a dataset.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID

        Returns:
            List of table dictionaries
        """
        result = self._make_request("GET", f"/groups/{workspace_id}/datasets/{dataset_id}/tables")
        tables = result.get("value", [])
        logger.info(f"Found {len(tables)} tables in dataset {dataset_id}")
        return tables

    def get_table(self, workspace_id: str, dataset_id: str, table_name: str) -> dict[str, Any]:
        """Get a specific table.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID
            table_name: Table name

        Returns:
            Table dictionary
        """
        result = self._make_request(
            "GET", f"/groups/{workspace_id}/datasets/{dataset_id}/tables/{table_name}"
        )
        logger.debug(f"Retrieved table {table_name} from dataset {dataset_id}")
        return result

    def get_relationships(self, workspace_id: str, dataset_id: str) -> list[dict[str, Any]]:
        """Get all relationships in a dataset.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID

        Returns:
            List of relationship dictionaries
        """
        result = self._make_request(
            "GET", f"/groups/{workspace_id}/datasets/{dataset_id}/relationships"
        )
        relationships = result.get("value", [])
        logger.info(f"Found {len(relationships)} relationships in dataset {dataset_id}")
        return relationships

    def get_measures(
        self, workspace_id: str, dataset_id: str, table_name: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """Get measures from a dataset or table.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID
            table_name: Optional table name to filter by

        Returns:
            List of measure dictionaries
        """
        endpoint = f"/groups/{workspace_id}/datasets/{dataset_id}/measures"
        if table_name:
            endpoint = f"/groups/{workspace_id}/datasets/{dataset_id}/tables/{table_name}/measures"
        result = self._make_request("GET", endpoint)
        measures = result.get("value", [])
        logger.info(f"Found {len(measures)} measures")
        return measures

    def get_columns(
        self, workspace_id: str, dataset_id: str, table_name: str
    ) -> list[dict[str, Any]]:
        """Get all columns in a table.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID
            table_name: Table name

        Returns:
            List of column dictionaries
        """
        result = self._make_request(
            "GET", f"/groups/{workspace_id}/datasets/{dataset_id}/tables/{table_name}/columns"
        )
        columns = result.get("value", [])
        logger.debug(f"Found {len(columns)} columns in table {table_name}")
        return columns

    def get_refresh_history(
        self, workspace_id: str, dataset_id: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Get refresh history for a dataset.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID
            limit: Maximum number of refreshes to return

        Returns:
            List of refresh history entries
        """
        result = self._make_request(
            "GET",
            f"/groups/{workspace_id}/datasets/{dataset_id}/refreshes",
            params={"$top": limit},
        )
        refreshes = result.get("value", [])
        logger.debug(f"Retrieved {len(refreshes)} refresh history entries")
        return refreshes

    def get_workspace(self, workspace_id: str) -> dict[str, Any]:
        """Get a specific workspace.

        Args:
            workspace_id: Workspace ID

        Returns:
            Workspace dictionary
        """
        result = self._make_request("GET", f"/groups/{workspace_id}")
        logger.debug(f"Retrieved workspace {workspace_id}")
        return result

    def execute_dax_query(
        self, workspace_id: str, dataset_id: str, dax_query: str
    ) -> dict[str, Any]:
        """Execute a DAX query against a dataset.

        Args:
            workspace_id: Workspace ID
            dataset_id: Dataset ID
            dax_query: DAX query string

        Returns:
            Query result dictionary
        """
        endpoint = f"/groups/{workspace_id}/datasets/{dataset_id}/executeQueries"
        payload = {"queries": [{"query": dax_query}]}
        result = self._make_request("POST", endpoint, json=payload)
        logger.debug(f"Executed DAX query on dataset {dataset_id}")
        return result

    def close(self) -> None:
        """Close the client connection."""
        self._access_token = None
        logger.info("Power BI client connection closed")

    def __enter__(self) -> "PowerBIClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
