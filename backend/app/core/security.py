"""Security helpers for JWT and password management."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a plain-text password using bcrypt."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash."""

    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        subject: Token subject, typically a user identifier.
        expires_delta: Optional custom expiry duration.
        additional_claims: Optional extra JWT claims.

    Returns:
        A signed JWT string.
    """

    payload: dict[str, Any] = {"sub": subject, "iat": datetime.now(timezone.utc)}
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    if additional_claims:
        payload.update(additional_claims)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_jwt_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token.

    Raises:
        JWTError: If the token is invalid or expired.
    """

    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
