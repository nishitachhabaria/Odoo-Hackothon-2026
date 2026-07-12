"""Authentication dependencies for protected endpoints."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the current authenticated user from a Bearer token."""

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token_payload = TokenData.model_validate(decode_access_token(credentials.credentials))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if token_payload.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repository = UserRepository(db)
    user = user_repository.get_by_id(token_payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensure the authenticated user account is active."""

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    return current_user


class RequireRole:
    """FastAPI dependency that enforces role-based authorization."""

    def __init__(self, *role_names: str) -> None:
        if not role_names:
            raise ValueError("At least one role name is required")
        self.role_names = {role_name.strip().lower() for role_name in role_names}

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """Validate that the authenticated user has one of the allowed roles."""

        user_role = current_user.role.name.lower() if current_user.role is not None else ""
        if user_role not in self.role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user
