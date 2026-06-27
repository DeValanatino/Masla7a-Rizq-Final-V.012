"""
Mock session token store.

Production replacement: JWT validation or Supabase Auth session lookup.
"""

from uuid import uuid4

from app.config import SESSION_TOKEN_PREFIX


class SessionRepository:
    """Maps mock session tokens to user IDs."""

    def __init__(self) -> None:
        self._token_to_user: dict[str, str] = {}

    def create_token(self, user_id: str) -> str:
        """Generate and persist a mock session token for the given user."""
        token = f"{SESSION_TOKEN_PREFIX}{uuid4().hex}"
        self._token_to_user[token] = user_id
        return token

    def get_user_id(self, token: str) -> str | None:
        """Resolve a session token to a user ID, or None if invalid."""
        return self._token_to_user.get(token)

    def revoke(self, token: str) -> None:
        """Invalidate a session token (logout)."""
        self._token_to_user.pop(token, None)
