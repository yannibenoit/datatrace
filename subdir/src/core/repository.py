"""DataTrace Base Repository Pattern.

Provides the base repository/DAO pattern for data access operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Any

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository class.

    Provides common CRUD operations and patterns for data access.
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity.

        Args:
            entity: Entity to create

        Returns:
            Created entity
        """
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[T]:
        """Get an entity by ID.

        Args:
            id: Entity ID

        Returns:
            Entity or None if not found
        """
        pass

    @abstractmethod
    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> list[T]:
        """Get all entities with optional pagination.

        Args:
            limit: Maximum number of entities to return
            offset: Offset for pagination

        Returns:
            List of entities
        """
        pass

    @abstractmethod
    def update(self, id: str, entity: T) -> Optional[T]:
        """Update an existing entity.

        Args:
            id: Entity ID
            entity: Updated entity data

        Returns:
            Updated entity or None if not found
        """
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete an entity.

        Args:
            id: Entity ID

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def exists(self, id: str) -> bool:
        """Check if an entity exists.

        Args:
            id: Entity ID

        Returns:
            True if exists, False otherwise
        """
        pass

    def get_by_field(self, field: str, value: Any) -> Optional[T]:
        """Get an entity by a specific field.

        Args:
            field: Field name to query
            value: Field value to match

        Returns:
            Entity or None if not found
        """
        # Default implementation - override for efficiency
        all_entities = self.get_all()
        for entity in all_entities:
            if getattr(entity, field, None) == value:
                return entity
        return None

    def get_all_by_field(self, field: str, value: Any) -> list[T]:
        """Get all entities matching a specific field value.

        Args:
            field: Field name to query
            value: Field value to match

        Returns:
            List of matching entities
        """
        all_entities = self.get_all()
        return [entity for entity in all_entities if getattr(entity, field, None) == value]
