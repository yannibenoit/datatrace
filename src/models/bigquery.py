"""DataTrace BigQuery Models.

BigQuery-specific models for tables and columns.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from datatrace.models.data_asset import DataAsset, DataAssetType, SourceType


class BigQueryTableType(str, Enum):
    """Type of BigQuery object."""

    TABLE = "TABLE"
    VIEW = "VIEW"
    MATERIALIZED_VIEW = "MATERIALIZED_VIEW"
    EXTERNAL = "EXTERNAL"


class BigQueryTable(DataAsset):
    """BigQuery table or view model.

    Specialization of DataAsset with BigQuery-specific attributes.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    # Override type to be BigQuery-specific
    type: DataAssetType = Field(
        DataAssetType.BIGQUERY_TABLE, description="Type of data asset", exclude=True
    )
    source_type: SourceType = Field(SourceType.BIGQUERY, description="The source system type")

    project_id: str = Field(..., max_length=255, description="Google Cloud project ID")
    dataset_id: str = Field(..., max_length=255, description="BigQuery dataset ID")
    table_type: BigQueryTableType = Field(..., description="Type of BigQuery object")
    partitioning: Optional[dict] = Field(None, description="Partitioning configuration")
    clustering: Optional[dict] = Field(None, description="Clustering configuration")
    storage_bytes: Optional[int] = Field(None, description="Storage used in bytes")
    row_count: Optional[int] = Field(None, description="Number of rows")
    last_modified: Optional[datetime] = Field(None, description="Last modification timestamp")
    created: Optional[datetime] = Field(None, description="Creation timestamp")
    expires: Optional[datetime] = Field(None, description="Expiration timestamp")


class BigQueryColumn(BaseModel):
    """BigQuery column model.

    Represents a column within a BigQuery table.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier")
    asset_id: str = Field(..., description="Reference to parent DataAsset (BigQueryTable)")
    column_name: str = Field(..., max_length=300, description="Column name")
    column_index: int = Field(..., description="Position in table (0-indexed)")
    data_type: str = Field(..., max_length=50, description="BigQuery data type")
    is_nullable: bool = Field(True, description="Whether column allows NULL")
    description: Optional[str] = Field(None, description="Column description")
    is_partitioning_column: bool = Field(False, description="Whether this is a partitioning column")
    is_clustering_column: bool = Field(False, description="Whether this is a clustering column")
    precision: Optional[int] = Field(None, description="Precision for numeric types")
    scale: Optional[int] = Field(None, description="Scale for numeric types")
    max_length: Optional[int] = Field(None, description="Maximum length for string types")
    is_pii: bool = Field(False, description="Whether this column contains PII")
    pii_category: Optional[str] = Field(None, max_length=50, description="PII category")
