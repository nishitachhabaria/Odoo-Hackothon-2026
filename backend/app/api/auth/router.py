"""Authentication API routes for AssetFlow."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth.schema import APIResponse, Token, UserCreate, UserLogin, UserResponse
from app.database.session import get_db
from app.dependencies.auth import RequireRole, get_current_active_user
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Create the authentication service for the current request."""

    return AuthService(UserRepository(db), RoleRepository(db))


@router.post("/signup", response_model=APIResponse[UserResponse], status_code=201)
def signup(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> APIResponse[UserResponse]:
    """Create an employee-only account.

    Users cannot select their own role; all signups are assigned the Employee
    role by the service layer.
    """

    user = auth_service.signup_employee(user_create)
    return APIResponse[UserResponse](message="Signup successful", data=UserResponse.model_validate(user))


@router.post("/login", response_model=APIResponse[Token])
def login(
    user_login: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> APIResponse[Token]:
    """Authenticate a user and return a JWT access token."""

    user = auth_service.authenticate(user_login)
    token = auth_service.create_token(user)
    token_response = Token(access_token=token, user=UserResponse.model_validate(user))
    return APIResponse[Token](message="Login successful", data=token_response)


@router.get("/me", response_model=APIResponse[UserResponse])
def read_me(current_user=Depends(get_current_active_user)) -> APIResponse[UserResponse]:
    """Return the current authenticated user profile."""

    return APIResponse[UserResponse](message="Current user retrieved", data=UserResponse.model_validate(current_user))


@router.post("/logout", response_model=APIResponse[dict[str, str]])
def logout(
    _current_user=Depends(RequireRole("Admin", "Employee", "Asset Manager", "Department Head")),
) -> APIResponse[dict[str, str]]:
    """Dummy logout endpoint for JWT clients."""

    return APIResponse[dict[str, str]](message="Logged out successfully", data={"message": "Logged out successfully"})
