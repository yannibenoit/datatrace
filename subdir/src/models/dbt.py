"""DataTrace dbt Models.

dbt-specific models for models and sources.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from datatrace.models.data_asset import DataAsset, DataAssetType, SourceType


class ResourceType(str, Enum):
    """dbt resource type."""

    MODEL = "model"
    SOURCE = "source"
    SEED = "seed"
    SNAPSHOT = "snapshot"
    ANALYSIS = "analysis"
    OPERATION = "operation"
    SINGULAR = "singular"
    HOOK = "hook"


class MaterializedType(str, Enum):
    """Materialization strategy."""

    TABLE = "table"
    VIEW = "view"
    INCREMENTAL = "incremental"
    EPHEMERAL = "ephemeral"
    MATERIALIZED_TABLE = "materialized_table"


class dbtModel(DataAsset):
    """dbt model entity.

    Specialization of DataAsset with dbt-specific attributes.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    # Override type to be dbt-specific
    type: DataAssetType = Field(
        DataAssetType.DBT_MODEL, description="Type of data asset", exclude=True
    )
    source_type: SourceType = Field(SourceType.DBT, description="The source system type")

    model_name: str = Field(..., max_length=255, description="dbt model name")
    resource_type: ResourceType = Field(..., description="dbt resource type")
    package_name: Optional[str] = Field(None, max_length=255, description="dbt package name")
    path: Optional[str] = Field(None, max_length=512, description="File path in dbt project")
    raw_sql: Optional[str] = Field(None, description="Raw SQL from model file")
    compiled_sql: Optional[str] = Field(None, description="Compiled SQL (after Jinja rendering)")
    database: Optional[str] = Field(None, max_length=255, description="Target database")
    schema: Optional[str] = Field(None, max_length=255, description="Target schema")
    alias: Optional[str] = Field(None, max_length=255, description="Model alias")
    materialized: MaterializedType = Field(..., description="Materialization strategy")
    config: Optional[dict] = Field(None, description="dbt model config")
    docs: Optional[dict] = Field(None, description="dbt documentation")
    meta: Optional[dict] = Field(None, description="dbt meta")
    tests: Optional[list] = Field(None, description="dbt tests")
    dependencies: Optional[list] = Field(None, description="List of dependencies")
    build_path: Optional[str] = Field(None, max_length=512, description="Build path in dbt artifacts")
    unique_id: Optional[str] = Field(None, max_length=512, description="dbt unique ID")
    patch_path: Optional[str] = Field(None, max_length=512, description="Patch path if applicable")
    buildable: bool = Field(True, description="Whether the model is buildable")
    checksum: Optional[dict] = Field(None, description="Checksum information")


class dbtSource(DataAsset):
    """dbt source definition.

    Specialization of DataAsset with dbt source-specific attributes.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    # Override type to be dbt-specific
    type: DataAssetType = Field(
        DataAssetType.DBT_SOURCE, description="Type of data asset", exclude=True
    )
    source_type: SourceType = Field(SourceType.DBT, description="The source system type")

    source_name: str = Field(..., max_length=255, description="dbt source name")
    table_name: str = Field(..., max_length=255, description="Source table name")
    database: Optional[str] = Field(None, max_length=255, description="Source database")
    schema: Optional[str] = Field(None, max_length=255, description="Source schema")
    identifier: Optional[str] = Field(None, max_length=512, description="Source identifier")
    quoting: Optional[dict] = Field(None, description="Quoting configuration")
    loaded_at_field: Optional[str] = Field(None, max_length=255, description="Field used for incremental loading")
    freshness: Optional[dict] = Field(None, description="Freshness configuration")
    external: Optional[dict] = Field(None, description="External configuration")
    description: Optional[str] = Field(None, description="Source description")
    columns: Optional[list] = Field(None, description="Column definitions")
    meta: Optional[dict] = Field(None, description="Source meta")
    source_definition_path: Optional[str] = Field(
        None, max_length=512, description="Path to source definition"
    )
    unrendered_config: Optional[dict] = Field(None, description="Unrendered source config")
