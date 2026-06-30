"""DataTrace Power BI Models.

Power BI-specific models for semantic models, tables, and relationships.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from datatrace.models.data_asset import DataAsset, DataAssetType, SourceType


class DefaultMode(str, Enum):
    """Default mode for Power BI semantic models."""

    PUSH = "Push"
    PULL = "Pull"
    LIVE_CONNECT = "LiveConnect"


class StorageMode(str, Enum):
    """Storage mode for Power BI semantic models."""

    IMPORT = "Import"
    DIRECT_QUERY = "DirectQuery"
    DUAL = "Dual"
    PUSH = "Push"


class Cardinality(str, Enum):
    """Relationship cardinality."""

    ONE_TO_MANY = "OneToMany"
    MANY_TO_ONE = "ManyToOne"
    ONE_TO_ONE = "OneToOne"
    MANY_TO_MANY = "ManyToMany"


class CrossFilterDirection(str, Enum):
    """Cross-filter direction."""

    ONE_WAY = "OneWay"
    BOTH = "Both"
    AUTOMATIC = "Automatic"


class PowerBISemanticModel(DataAsset):
    """Power BI semantic model (formerly dataset).

    Specialization of DataAsset with Power BI-specific attributes.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    # Override type to be Power BI-specific
    type: DataAssetType = Field(
        DataAssetType.POWERBI_SEMANTIC_MODEL, description="Type of data asset", exclude=True
    )
    source_type: SourceType = Field(SourceType.POWERBI, description="The source system type")

    workspace_id: str = Field(..., description="Power BI workspace ID")
    workspace_name: Optional[str] = Field(None, max_length=255, description="Power BI workspace name")
    dataset_id: str = Field(..., description="Power BI dataset ID")
    dataset_name: str = Field(..., max_length=255, description="Power BI dataset name")
    configured_by: Optional[str] = Field(None, max_length=255, description="Who configured the semantic model")
    default_mode: Optional[DefaultMode] = Field(None, description="Default mode")
    storage_mode: Optional[StorageMode] = Field(None, description="Storage mode")
    refresh_schedule: Optional[dict] = Field(None, description="Refresh schedule")
    last_refresh: Optional[datetime] = Field(None, description="Last refresh timestamp")
    tables: Optional[list] = Field(None, description="List of tables in semantic model")
    relationships: Optional[list] = Field(None, description="Relationships between tables")
    measures: Optional[list] = Field(None, description="Measures defined in semantic model")
    columns: Optional[list] = Field(None, description="Columns with their properties")
    culture: Optional[str] = Field(None, max_length=10, description="Locale/culture")
    collation: Optional[str] = Field(None, max_length=20, description="Collation setting")


class PowerBITable(BaseModel):
    """Power BI table model.

    Represents a table within a Power BI semantic model.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier")
    semantic_model_id: str = Field(..., description="Reference to PowerBISemanticModel")
    name: str = Field(..., max_length=255, description="Table name")
    display_name: Optional[str] = Field(None, max_length=255, description="Display name")
    description: Optional[str] = Field(None, description="Table description")
    is_hidden: bool = Field(False, description="Whether table is hidden")
    row_count: Optional[int] = Field(None, description="Number of rows")
    columns: Optional[list] = Field(None, description="List of columns")
    measures: Optional[list] = Field(None, description="List of measures")
    hierarchies: Optional[list] = Field(None, description="Hierarchies defined")


class PowerBIRelationship(BaseModel):
    """Power BI relationship model.

    Represents a relationship between tables in a Power BI semantic model.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier")
    semantic_model_id: str = Field(..., description="Reference to PowerBISemanticModel")
    name: str = Field(..., max_length=255, description="Relationship name")
    from_table: str = Field(..., max_length=255, description="Source table name")
    from_column: str = Field(..., max_length=255, description="Source column name")
    to_table: str = Field(..., max_length=255, description="Target table name")
    to_column: str = Field(..., max_length=255, description="Target column name")
    cardinality: Cardinality = Field(..., description="Relationship cardinality")
    cross_filter_direction: CrossFilterDirection = Field(
        ..., description="Cross-filter direction"
    )
    is_active: bool = Field(True, description="Whether relationship is active")
