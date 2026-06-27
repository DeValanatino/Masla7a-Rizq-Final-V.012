"""
Authentication service — register-or-login flow.

Handles new user registration with trial subscription and returning user login.
"""

from datetime import date, timedelta

from fastapi import HTTPException, status

from app.config import DEFAULT_TRIAL_DAYS
from app.models.user import User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, RegisterOrLoginRequest


class AuthService:
    """Phone-first register/login orchestration."""

    def __init__(
        self,
        user_repo: UserRepository,
        session_repo: SessionRepository,
    ) -> None:
        self._users = user_repo
        self._sessions = session_repo

    def register_or_login(self, payload: RegisterOrLoginRequest) -> AuthResponse:
        """
        Register a new user or log in an existing one by phone number.

        New users receive a DEFAULT_TRIAL_DAYS trial subscription window.
        """
        existing = self._users.get_by_phone(payload.phone_number)

        if existing:
            token = self._sessions.create_token(existing.id)
            return AuthResponse(
                session_token=token,
                user_id=existing.id,
                phone_number=existing.phone_number,
                name=existing.name,
                account_type=existing.account_type,
                is_new_user=False,
                subscription_expiry_date=(
                    existing.subscription_expiry_date.isoformat()
                ),
                subscription_active=existing.is_subscription_active,
            )

        # --- New registration path ---
        if not payload.name or not payload.account_type:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "New users must provide both 'name' and 'account_type'. "
                    "Account types: Factory, Workshop, Gallery, Project Manager, Craftsman, Worker"
                ),
            )

        trial_expiry = date.today() + timedelta(days=DEFAULT_TRIAL_DAYS)
        new_user = User(
            phone_number=payload.phone_number,
            name=payload.name,
            account_type=payload.account_type,
            subscription_expiry_date=trial_expiry,
        )
        self._users.save(new_user)

        token = self._sessions.create_token(new_user.id)
        return AuthResponse(
            session_token=token,
            user_id=new_user.id,
            phone_number=new_user.phone_number,
            name=new_user.name,
            account_type=new_user.account_type,
            is_new_user=True,
            subscription_expiry_date=new_user.subscription_expiry_date.isoformat(),
            subscription_active=new_user.is_subscription_active,
        )
