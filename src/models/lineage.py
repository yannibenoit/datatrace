"""DataTrace Lineage Edge Model.

Represents a relationship/edge in the lineage graph, connecting source and
target data assets with a relationship type.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class RelationshipType(str, Enum):
    """Type of relationship in lineage."""

    TRANSFORMS = "transforms"
    DEPENDS_ON = "depends_on"
    FEEDS_INTO = "feeds_into"
    REFERENCES = "references"
    MATERIALIZES = "materializes"
    COPIES = "copies"
    AGGREGATES = "aggregates"


class VerificationStatus(str, Enum):
    """Verification status for lineage edges."""

    AUTO_DISCOVERED = "auto_discovered"
    VERIFIED = "verified"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"


class LineageEdge(BaseModel):
    """Lineage edge model.

    Represents a relationship in the lineage graph.
    """

    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(..., description="Unique identifier for the lineage edge")
    source_id: str = Field(..., description="Reference to source DataAsset")
    target_id: str = Field(..., description="Reference to target DataAsset")
    relationship_type: RelationshipType = Field(..., description="Type of relationship")
    transformation_type: Optional[str] = Field(
        None, max_length=50, description="Specific transformation type"
    )
    column_mapping: Optional[dict] = Field(None, description="Column-level lineage mapping")
    sql_logic: Optional[str] = Field(None, description="SQL logic if applicable")
    metadata: Optional[dict] = Field(None, description="Additional edge metadata")
    discovered_at: datetime = Field(..., description="When the lineage was discovered")
    verified_at: Optional[datetime] = Field(None, description="When the lineage was manually verified")
    verification_status: VerificationStatus = Field(
        ..., description="Verification status"
    )
    is_production: bool = Field(True, description="Whether this lineage is production-ready")
