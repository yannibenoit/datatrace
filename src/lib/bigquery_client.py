"""BigQuery Client for DataTrace.

Provides connection and query utilities for BigQuery integration.
"""

import logging
from typing import Optional, Any

from google.cloud import bigquery
from google.cloud.bigquery import QueryJob, Table
from google.cloud.exceptions import GoogleCloudError

from datatrace.lib.exceptions import ConnectionError, DiscoveryError

logger = logging.getLogger(__name__)


class BigQueryClient:
    """BigQuery client for DataTrace operations.

    Handles connection management, metadata queries, and data extraction.
    """

    def __init__(self, project_id: str, credentials_path: Optional[str] = None):
        """Initialize BigQuery client.

        Args:
            project_id: Google Cloud project ID
            credentials_path: Optional path to service account credentials JSON
        """
        self.project_id = project_id
        self.credentials_path = credentials_path
        self._client: Optional[bigquery.Client] = None

    @property
    def client(self) -> bigquery.Client:
        """Get or create BigQuery client."""
        if self._client is None:
            try:
                if self.credentials_path:
                    self._client = bigquery.Client.from_service_account_json(
                        self.credentials_path, project=self.project_id
                    )
                else:
                    self._client = bigquery.Client(project=self.project_id)
                logger.info(f"BigQuery client initialized for project: {self.project_id}")
            except GoogleCloudError as e:
                logger.error(f"Failed to initialize BigQuery client: {e}")
                raise ConnectionError(f"BigQuery connection failed: {e}")
        return self._client

    def execute_query(self, query: str, params: Optional[list] = None) -> QueryJob:
        """Execute a SQL query.

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            QueryJob with results
        """
        try:
            job_config = bigquery.QueryJobConfig()
            if params:
                job_config.query_parameters = params

            query_job = self.client.query(query, job_config=job_config)
            query_job.result()  # Wait for completion
            logger.debug(f"Query executed successfully: {query[:100]}...")
            return query_job
        except GoogleCloudError as e:
            logger.error(f"Query execution failed: {e}")
            raise DiscoveryError(f"Query failed: {e}")

    def get_table(self, dataset_id: str, table_id: str) -> Table:
        """Get a BigQuery table.

        Args:
            dataset_id: Dataset ID
            table_id: Table ID

        Returns:
            BigQuery Table object
        """
        try:
            table_ref = self.client.dataset(dataset_id).table(table_id)
            table = self.client.get_table(table_ref)
            logger.debug(f"Retrieved table: {dataset_id}.{table_id}")
            return table
        except GoogleCloudError as e:
            logger.error(f"Failed to get table {dataset_id}.{table_id}: {e}")
            raise DiscoveryError(f"Table retrieval failed: {e}")

    def list_datasets(self) -> list[str]:
        """List all datasets in the project.

        Returns:
            List of dataset IDs
        """
        try:
            datasets = list(self.client.list_datasets())
            dataset_ids = [ds.dataset_id for ds in datasets]
            logger.info(f"Found {len(dataset_ids)} datasets in project {self.project_id}")
            return dataset_ids
        except GoogleCloudError as e:
            logger.error(f"Failed to list datasets: {e}")
            raise DiscoveryError(f"Dataset listing failed: {e}")

    def list_tables(self, dataset_id: str) -> list[str]:
        """List all tables in a dataset.

        Args:
            dataset_id: Dataset ID

        Returns:
            List of table IDs
        """
        try:
            tables = list(self.client.list_tables(dataset_id))
            table_ids = [t.table_id for t in tables]
            logger.info(f"Found {len(table_ids)} tables in dataset {dataset_id}")
            return table_ids
        except GoogleCloudError as e:
            logger.error(f"Failed to list tables in {dataset_id}: {e}")
            raise DiscoveryError(f"Table listing failed: {e}")

    def get_table_metadata(self, dataset_id: str, table_id: str) -> dict[str, Any]:
        """Get comprehensive metadata for a table.

        Args:
            dataset_id: Dataset ID
            table_id: Table ID

        Returns:
            Dictionary with table metadata
        """
        try:
            table = self.get_table(dataset_id, table_id)
            return {
                "table_id": table.table_id,
                "dataset_id": table.dataset_id,
                "project_id": table.project,
                "description": table.description,
                "created": table.created.isoformat() if table.created else None,
                "modified": table.modified.isoformat() if table.modified else None,
                "row_count": table.num_rows,
                "storage_bytes": table.num_bytes,
                "schema": [
                    {
                        "name": field.name,
                        "type": field.field_type,
                        "mode": field.mode,
                        "description": field.description,
                    }
                    for field in table.schema
                ],
            }
        except Exception as e:
            logger.error(f"Failed to get metadata for {dataset_id}.{table_id}: {e}")
            raise DiscoveryError(f"Metadata retrieval failed: {e}")

    def query_information_schema(
        self, query_type: str, dataset_id: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """Query INFORMATION_SCHEMA views.

        Args:
            query_type: Type of information to query (TABLES, COLUMNS, TABLE_STORAGE, etc.)
            dataset_id: Optional dataset filter

        Returns:
            List of results
        """
        valid_types = ["TABLES", "COLUMNS", "TABLE_STORAGE", "VIEWS", "ROUTINES", "JOBS"]
        if query_type not in valid_types:
            raise ValueError(f"Invalid query_type: {query_type}. Must be one of {valid_types}")

        dataset_filter = f"AND table_schema = '{dataset_id}'" if dataset_id else ""

        query = f"""
            SELECT * 
            FROM `{self.project_id}.INFORMATION_SCHEMA.{query_type}`
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            {dataset_filter}
        """

        job = self.execute_query(query)
        results = []
        for row in job.result():
            results.append(dict(row))
        return results

    def close(self) -> None:
        """Close the BigQuery client connection."""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("BigQuery client connection closed")

    def __enter__(self) -> "BigQueryClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
