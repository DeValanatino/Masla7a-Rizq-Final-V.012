"""
User domain model.

Mirrors the future Supabase `users` table:
  id, phone_number, name, account_type, subscription_expiry_date
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class AccountType(str, Enum):
    """General account classification — informational only, never a permission lock."""

    FACTORY = "Factory"
    WORKSHOP = "Workshop"
    GALLERY = "Gallery"
    PROJECT_MANAGER = "Project Manager"
    CRAFTSMAN = "Craftsman"
    WORKER = "Worker"


@dataclass
class User:
    """In-memory representation of a marketplace user."""

    phone_number: str
    name: str
    account_type: AccountType
    subscription_expiry_date: date
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------
    # Subscription helpers
    # ------------------------------------------------------------------

    @property
    def is_subscription_active(self) -> bool:
        """Return True when the 200 EGP subscription window is still open."""
        return date.today() <= self.subscription_expiry_date

    # ------------------------------------------------------------------
    # Serialization — keeps repository layer DB-agnostic
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict (Supabase insert/update friendly)."""
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "name": self.name,
            "account_type": self.account_type.value,
            "subscription_expiry_date": self.subscription_expiry_date.isoformat(),
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        """Hydrate a User from a dict (future Supabase row)."""
        return cls(
            id=data["id"],
            phone_number=data["phone_number"],
            name=data["name"],
            account_type=AccountType(data["account_type"]),
            subscription_expiry_date=date.fromisoformat(data["subscription_expiry_date"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
