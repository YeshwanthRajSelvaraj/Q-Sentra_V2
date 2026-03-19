"""
Q-Sentra Authentication Routes
JWT login, token refresh, and user profile.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from core.security import (
    DEMO_USERS, verify_password, create_access_token,
    get_current_user, require_role
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """Authenticate user and return JWT token."""
    user = DEMO_USERS.get(req.username)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"],
        "user_id": user["user_id"],
    })

    return TokenResponse(
        access_token=token,
        user={
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"],
            "full_name": user["full_name"],
        }
    )


@router.get("/me")
async def get_profile(user: dict = Depends(get_current_user)):
    """Get current user profile."""
    demo_user = DEMO_USERS.get(user["username"], {})
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "full_name": demo_user.get("full_name", user["username"]),
    }


@router.get("/users")
async def list_users(user: dict = Depends(require_role("admin"))):
    """List all users (admin only)."""
    return [
        {"user_id": u["user_id"], "username": u["username"], "role": u["role"], "full_name": u["full_name"]}
        for u in DEMO_USERS.values()
    ]
