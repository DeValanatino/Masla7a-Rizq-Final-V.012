"""
Application-wide configuration.

Centralize constants here so they can later be loaded from environment
variables or a Supabase-backed settings table without touching route logic.
"""

from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ---------------------------------------------------------------------------
# Gemini API Configuration
# ---------------------------------------------------------------------------
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
"""API key for Gemini; automatically loaded from environment."""


# ---------------------------------------------------------------------------
# Subscription / Gatekeeper (200 EGP monthly access)
# ---------------------------------------------------------------------------
SUBSCRIPTION_PRICE_EGP: int = 200
"""Monthly subscription fee shown in lockout responses."""

DEFAULT_TRIAL_DAYS: int = 30
"""Free trial granted to newly registered users."""

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
EGYPTIAN_PHONE_LENGTH: int = 11
"""Egyptian mobile numbers are exactly 11 digits (e.g. 01012345678)."""

SESSION_TOKEN_PREFIX: str = "msla7a_"
"""Prefix for mock session tokens; replace with JWT in production."""

# ---------------------------------------------------------------------------
# Feed defaults
# ---------------------------------------------------------------------------
DEFAULT_FEED_LIMIT: int = 50
"""Maximum items returned per track in the unified feed."""
