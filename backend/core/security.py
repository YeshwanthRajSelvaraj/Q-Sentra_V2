"""
Q-Sentra Security Module
JWT authentication, password hashing, and RBAC middleware.
"""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import get_settings

settings = get_settings()

# ── Password Hashing (SHA-256 for prototype; use Argon2 in production) ──
_SALT = "qsentra-salt-2026"
security_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a plaintext password using SHA-256 with salt."""
    return hashlib.sha256(f"{_SALT}{password}".encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(plain) == hashed


# ── JWT Token Management ──
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with claims."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_EXPIRY_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# ── Auth Dependencies ──
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict:
    """FastAPI dependency: extracts and validates the current user from JWT."""
    payload = decode_token(credentials.credentials)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {
        "username": username,
        "role": payload.get("role", "analyst"),
        "user_id": payload.get("user_id", "1"),
    }


def require_role(*allowed_roles):
    """Factory: returns a dependency that enforces RBAC."""
    async def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user['role']}' not authorized. Required: {allowed_roles}"
            )
        return user
    return role_checker


# ── Demo Users (in-memory for prototype) ──
DEMO_USERS = {
    "admin": {
        "user_id": "1",
        "username": "admin",
        "password_hash": hash_password("admin123"),
        "role": "admin",
        "full_name": "System Administrator",
    },
    "analyst": {
        "user_id": "2",
        "username": "analyst",
        "password_hash": hash_password("analyst123"),
        "role": "analyst",
        "full_name": "Security Analyst",
    },
    "devops": {
        "user_id": "3",
        "username": "devops",
        "password_hash": hash_password("devops123"),
        "role": "devops",
        "full_name": "DevOps Engineer",
    },
}


# ── Vault Mock ──
class VaultMock:
    """Simulates HashiCorp Vault for secrets management."""

    _secrets = {
        "db/postgres": {"username": "qsentra", "password": "qsentra_pass"},
        "db/mongo": {"username": "root", "password": "mongo_pass"},
        "crypto/aes_key": {"key": hashlib.sha256(b"qsentra-aes-key").hexdigest()},
        "jwt/secret": {"key": settings.JWT_SECRET},
    }

    @classmethod
    def read_secret(cls, path: str) -> dict:
        """Read a secret from the mock vault."""
        if path in cls._secrets:
            return {"data": cls._secrets[path], "lease_duration": 3600}
        raise ValueError(f"Secret not found: {path}")

    @classmethod
    def write_secret(cls, path: str, data: dict):
        """Write a secret to the mock vault."""
        cls._secrets[path] = data

    @classmethod
    def encrypt_transit(cls, plaintext: str) -> str:
        """Simulate AES-256 transit encryption."""
        import base64
        return base64.b64encode(
            hashlib.sha256(plaintext.encode()).digest()
        ).decode()
