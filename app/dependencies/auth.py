"""
Phone-number authentication gatekeeper.

Every protected endpoint resolves the caller via Bearer session token.
This is the strict phone-auth gate before any dashboard action.
"""

from fastapi import Depends, Header, HTTPException, status

from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository


def get_session_repo() -> SessionRepository:
    """Provide the shared session repository (wired in main.py)."""
    from app.main import session_repo
    return session_repo


def get_user_repo() -> UserRepository:
    """Provide the shared user repository (wired in main.py)."""
    from app.main import user_repo
    return user_repo


async def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    sessions: SessionRepository = Depends(get_session_repo),
    users: UserRepository = Depends(get_user_repo),
) -> User:
    """
    Resolve the authenticated user from a Bearer session token.

    Raises:
        HTTPException 401: Missing, malformed, or expired token.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide Authorization: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    user_id = sessions.get_user_id(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = users.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found for this session",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
