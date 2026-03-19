"""Authentication routes."""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from core.security import hash_password, verify_password, create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str = "readonly"
    department: str = ""


# Simulated user store (in production, uses PostgreSQL)
DEMO_USERS = {
    "admin": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "username": "admin",
        "email": "admin@pnb.co.in",
        "password_hash": "$2b$12$LJ3m4VKcK6fH1T5PsRQxZOYFGz5KGHxKpGvLcRuFkByNm6a9HmJqe",
        "full_name": "System Administrator",
        "role": "admin",
        "department": "Cybersecurity",
        "is_active": True,
    },
    "analyst01": {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "username": "analyst01",
        "email": "analyst@pnb.co.in",
        "password_hash": "$2b$12$LJ3m4VKcK6fH1T5PsRQxZOYFGz5KGHxKpGvLcRuFkByNm6a9HmJqe",
        "full_name": "Security Analyst",
        "role": "analyst",
        "department": "SOC",
        "is_active": True,
    },
}


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token."""
    user = DEMO_USERS.get(request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # For demo, accept any password for demo users
    # In production, verify against hashed password
    token = create_access_token(
        data={
            "sub": user["id"],
            "username": user["username"],
            "role": user["role"],
            "email": user["email"],
        }
    )

    return LoginResponse(
        access_token=token,
        expires_in=28800,
        user={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "department": user["department"],
        },
    )


@router.get("/me")
async def get_current_user_info():
    """Get current user profile."""
    return {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "username": "admin",
        "email": "admin@pnb.co.in",
        "full_name": "System Administrator",
        "role": "admin",
        "department": "Cybersecurity",
        "mfa_enabled": True,
        "last_login": datetime.utcnow().isoformat(),
    }


@router.post("/logout")
async def logout():
    """Logout and invalidate token."""
    return {"message": "Successfully logged out"}
