"""DataTrace Classification Tag Model.

Classification tags for PII/PDS and sensitivity classification.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SensitivityLevel(str, Enum):
    """Sensitivity level for classification."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ClassificationTag(BaseModel):
    """Classification tag model.

    Used for tagging columns or assets with classification information.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier")
    column_id: Optional[str] = Field(None, description="Reference to column (if column-level)")
    asset_id: Optional[str] = Field(None, description="Reference to asset (if asset-level)")
    tag: str = Field(..., max_length=50, description="Classification tag")
    sensitivity: SensitivityLevel = Field(..., description="Sensitivity level")
    mask_pattern: Optional[str] = Field(None, max_length=100, description="Masking pattern")
    created_at: datetime = Field(..., description="When the classification was created")
    updated_at: datetime = Field(..., description="When the classification was last updated")
