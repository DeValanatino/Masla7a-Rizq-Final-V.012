"""Authentication request and response schemas."""

import re

from pydantic import BaseModel, Field, field_validator

from app.config import EGYPTIAN_PHONE_LENGTH
from app.models.user import AccountType


class RegisterOrLoginRequest(BaseModel):
    """
    Phone-first auth payload.

    New users must supply name and account_type; returning users need only
    their 11-digit Egyptian phone number.
    """

    phone_number: str = Field(
        ...,
        description="11-digit Egyptian mobile number (e.g. 01012345678)",
        examples=["01012345678"],
    )
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
        description="Display name — required for new registrations",
    )
    account_type: AccountType | None = Field(
        default=None,
        description="General account classification — required for new registrations",
    )

    @field_validator("phone_number")
    @classmethod
    def validate_egyptian_phone(cls, value: str) -> str:
        """Enforce strict 11-digit Egyptian phone format."""
        cleaned = value.strip().replace(" ", "").replace("-", "")
        if not re.fullmatch(r"\d{11}", cleaned):
            raise ValueError(
                f"Phone number must be exactly {EGYPTIAN_PHONE_LENGTH} digits"
            )
        if not cleaned.startswith("01"):
            raise ValueError("Egyptian mobile numbers must start with 01")
        return cleaned


class AuthResponse(BaseModel):
    """Successful authentication response with mock session token."""

    session_token: str
    user_id: str
    phone_number: str
    name: str
    account_type: AccountType
    is_new_user: bool
    subscription_expiry_date: str
    subscription_active: bool
