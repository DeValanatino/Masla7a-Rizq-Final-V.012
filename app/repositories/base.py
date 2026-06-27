"""
Abstract repository contract.

Every concrete repository implements this interface so services remain
unaware of whether data lives in memory or Supabase.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Minimal CRUD surface shared by all repositories."""

    @abstractmethod
    def get_by_id(self, entity_id: str) -> T | None:
        """Fetch a single entity by primary key."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """Insert or update an entity."""

    @abstractmethod
    def list_all(self) -> list[T]:
        """Return every entity (use pagination in production)."""
