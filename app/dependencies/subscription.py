"""
The 200 EGP subscription gatekeeper.

Blocks access to the unified feed when subscription_expiry_date has passed.
Returns a hard JSON lockout response with renewal instructions.
"""

from datetime import date

from fastapi import Depends, HTTPException, status

from app.config import SUBSCRIPTION_PRICE_EGP
from app.dependencies.auth import get_current_user
from app.models.user import User


async def require_active_subscription(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency that enforces the 200 EGP monthly subscription gate.

    Apply this ONLY to endpoints that require paid access (unified feed).
    Project creation and asset sharing remain accessible to authenticated
    users regardless of subscription — they can build from their dashboard
    but cannot browse the marketplace grid until renewed.

    Raises:
        HTTPException 402: Subscription expired — hard lockout response.
    """
    if not current_user.is_subscription_active:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "locked": True,
                "message_ar": (
                    "انتهت صلاحية اشتراكك. يرجى تجديد اشتراك مصلحة رزق "
                    f"بقيمة {SUBSCRIPTION_PRICE_EGP} جنيه للوصول إلى لوحة العرض الموحدة."
                ),
                "message_en": (
                    "Your Msla7a Rizq subscription has expired. "
                    f"Renew for {SUBSCRIPTION_PRICE_EGP} EGP to unlock the unified feed."
                ),
                "subscription_price_egp": SUBSCRIPTION_PRICE_EGP,
                "subscription_expiry_date": (
                    current_user.subscription_expiry_date.isoformat()
                ),
                "renewal_required": True,
            },
        )

    return current_user
