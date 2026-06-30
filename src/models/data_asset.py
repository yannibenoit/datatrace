"""DataTrace Data Asset Model.

Represents a generic entity for any data source, transformation, or destination.
This is the base entity from which all other data entities inherit.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class DataAssetType(str, Enum):
    """Type of data asset."""

    BIGQUERY_TABLE = "bigquery_table"
    BIGQUERY_VIEW = "bigquery_view"
    DBT_MODEL = "dbt_model"
    DBT_SOURCE = "dbt_source"
    DBT_SEED = "dbt_seed"
    DBT_SNAPSHOT = "dbt_snapshot"
    POWERBI_SEMANTIC_MODEL = "powerbi_semantic_model"
    POWERBI_REPORT = "powerbi_report"
    EXTERNAL_DATABASE = "external_database"
    API = "api"
    FILE = "file"


class SourceType(str, Enum):
    """The source system type."""

    BIGQUERY = "bigquery"
    DBT = "dbt"
    POWERBI = "powerbi"
    OTHER = "other"


class DataAsset(BaseModel):
    """Base data asset model.

    A generic entity representing any data source, transformation, or destination.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier for the data asset")
    name: str = Field(..., max_length=255, description="Human-readable name")
    type: DataAssetType = Field(..., description="Type of data asset")
    description: Optional[str] = Field(None, description="Detailed description")
    source_type: SourceType = Field(..., description="The source system type")
    connection_id: Optional[str] = Field(None, description="Reference to connection configuration")
    created_at: datetime = Field(..., description="When the asset was first cataloged")
    updated_at: datetime = Field(..., description="When the asset was last updated")
    is_active: bool = Field(True, description="Whether the asset is actively tracked")
    external_id: Optional[str] = Field(
        None, max_length=512, description="External identifier (e.g., BigQuery table ID)"
    )
