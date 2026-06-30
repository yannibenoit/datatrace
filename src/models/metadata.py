"""DataTrace Metadata Model.

Stores metadata about data assets including owner, description, schema,
data type, freshness expectations, and classification level.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class DataType(str, Enum):
    """Type of the metadata value."""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    JSON = "json"
    DATE = "date"
    TIMESTAMP = "timestamp"


class MetadataSource(str, Enum):
    """Source of this metadata."""

    AUTO_DISCOVERED = "auto_discovered"
    MANUAL = "manual"
    DBT = "dbt"
    POWERBI = "powerbi"
    USER_PROVIDED = "user_provided"


class Classification(str, Enum):
    """Classification category."""

    PII = "PII"
    PDS = "PDS"
    CONFIDENTIAL = "confidential"
    INTERNAL = "internal"
    PUBLIC = "public"


class SensitivityLevel(str, Enum):
    """Sensitivity level."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Metadata(BaseModel):
    """Metadata model for data assets.

    Every data asset must have metadata.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier for the metadata entry")
    asset_id: str = Field(..., description="Reference to the DataAsset")
    key: str = Field(..., max_length=100, description="Metadata key")
    value: Optional[str] = Field(None, description="Metadata value (stored as JSON string for structured data)")
    data_type: DataType = Field(..., description="Type of the value")
    source: MetadataSource = Field(..., description="Source of this metadata")
    classification: Optional[Classification] = Field(None, description="Classification category")
    sensitivity_level: Optional[SensitivityLevel] = Field(None, description="Sensitivity level")
    created_at: datetime = Field(..., description="When the metadata was created")
    updated_at: datetime = Field(..., description="When the metadata was last updated")
