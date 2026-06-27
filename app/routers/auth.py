"""
Authentication routes.

POST /auth/register_or_login — phone-first gatekeeper entry point.
"""

from fastapi import APIRouter, Depends

from app.schemas.auth import AuthResponse, RegisterOrLoginRequest
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


def _get_auth_service() -> AuthService:
    from app.main import session_repo, user_repo
    return AuthService(user_repo=user_repo, session_repo=session_repo)


@router.post(
    "/register_or_login",
    response_model=AuthResponse,
    summary="Register or login with Egyptian phone number",
    description=(
        "Accepts an 11-digit Egyptian phone number. "
        "Registers new users (requires name + account_type) or logs in existing users. "
        "Returns a mock session token for subsequent authenticated requests."
    ),
)
def register_or_login(
    payload: RegisterOrLoginRequest,
    auth_service: AuthService = Depends(_get_auth_service),
) -> AuthResponse:
    """Phone-number authentication gate — the front door to Msla7a Rizq."""
    return auth_service.register_or_login(payload)
