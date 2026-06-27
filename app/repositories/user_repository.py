"""
In-memory user repository.

Supabase migration path:
  replace method bodies with supabase.table("users").select/insert/update calls
  while keeping the same public method signatures.
"""

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Phone-indexed in-memory store for User records."""

    def __init__(self) -> None:
        self._by_id: dict[str, User] = {}
        self._by_phone: dict[str, User] = {}

    def get_by_id(self, user_id: str) -> User | None:
        return self._by_id.get(user_id)

    def get_by_phone(self, phone_number: str) -> User | None:
        """Lookup user by Egyptian phone number (unique key)."""
        return self._by_phone.get(phone_number)

    def save(self, user: User) -> User:
        self._by_id[user.id] = user
        self._by_phone[user.phone_number] = user
        return user

    def list_all(self) -> list[User]:
        return list(self._by_id.values())
