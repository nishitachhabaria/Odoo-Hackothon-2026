"""Authentication service layer for AssetFlow."""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData, UserCreate, UserLogin


class AuthService:
    """Coordinate authentication, token creation, and signup flows."""

    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository) -> None:
        self.user_repository = user_repository
        self.role_repository = role_repository

    def seed_default_data(self) -> None:
        """Create the default RBAC roles and the bootstrap admin user."""

        default_roles = (
            ("Admin", "Full platform access with role management permissions."),
            ("Employee", "Default employee account for standard access."),
            ("Asset Manager", "Manages assets and allocation workflows."),
            ("Department Head", "Oversees department-level approvals and access."),
        )
        for role_name, description in default_roles:
            self.role_repository.get_or_create(role_name, description)

        admin_email = "admin@assetflow.com"
        if self.user_repository.exists_by_email(admin_email):
            return

        admin_role = self.role_repository.get_by_name("Admin")
        if admin_role is None:
            raise RuntimeError("Default Admin role is missing")

        admin_user = User(
            first_name="System",
            last_name="Administrator",
            email=admin_email,
            phone=None,
            password_hash=get_password_hash("Admin@123"),
            department_id=None,
            role_id=admin_role.id,
            status="active",
            is_active=True,
        )
        self.user_repository.create(admin_user)

    def signup_employee(self, user_create: UserCreate) -> User:
        """Create a new user with the default Employee role."""

        if self.user_repository.exists_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        employee_role = self.role_repository.get_by_name("Employee")
        if employee_role is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Default Employee role is unavailable",
            )

        user = User(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            email=user_create.email,
            phone=user_create.phone,
            password_hash=get_password_hash(user_create.password),
            department_id=None,
            role_id=employee_role.id,
            status="active",
            is_active=True,
        )
        return self.user_repository.create(user)

    def authenticate(self, user_login: UserLogin) -> User:
        """Authenticate a user using email and password."""

        user = self.user_repository.get_by_email(user_login.email)
        if user is None or not verify_password(user_login.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        return user

    def create_token(self, user: User) -> str:
        """Create a JWT token for a user."""

        return create_access_token(
            subject=str(user.id),
            additional_claims={
                "email": user.email,
                "role": user.role.name if user.role is not None else None,
            },
        )

    def resolve_token_data(self, token: str) -> TokenData:
        """Decode a JWT token into strongly typed claims."""

        from app.core.security import decode_access_token

        return TokenData.model_validate(decode_access_token(token))

    @staticmethod
    def user_id_from_token(token_data: TokenData) -> UUID:
        """Extract the user UUID from decoded token data."""

        if token_data.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data.user_id
