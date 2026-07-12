"""Authentication and RBAC schemas for AssetFlow."""

from __future__ import annotations

import re
from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.department import DepartmentReference

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$")


class RoleResponse(BaseModel):
    """Role payload returned by the API."""

    id: int
    name: str
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Payload used to create a new employee account."""

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str
    phone: str | None = Field(default=None, max_length=30)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("first_name", "last_name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        """Normalize name fields by trimming whitespace."""

        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """Validate and normalize the email address."""

        normalized = value.strip().lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValueError("A valid email address is required")
        return normalized

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str | None) -> str | None:
        """Trim phone values when provided."""

        return value.strip() if value else value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Enforce a strong password policy."""

        if not PASSWORD_PATTERN.match(value):
            raise ValueError(
                "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"
            )
        return value


class UserLogin(BaseModel):
    """Login payload for JWT authentication."""

    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_login_email(cls, value: str) -> str:
        """Validate and normalize the login email."""

        normalized = value.strip().lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValueError("A valid email address is required")
        return normalized


class UserResponse(BaseModel):
    """User payload returned to clients."""

    id: UUID
    first_name: str
    last_name: str
    email: str
    employee_code: str | None = None
    designation: str | None = None
    joining_date: date | None = None
    phone: str | None = None
    profile_image: str | None = None
    department_id: UUID | None = None
    department: DepartmentReference | None = None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT response payload."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Decoded JWT claims used by the authentication dependency layer."""

    user_id: UUID | None = Field(default=None, alias="sub")
    email: str | None = None
    role: str | None = None

    model_config = ConfigDict(populate_by_name=True)
