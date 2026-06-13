# backend/app/core/security.py
# PURPOSE: JWT token creation and verification.
#
# This file is the security core of your application.
# It has two jobs:
#   1. Create a JWT token when user logs in
#   2. Decode and verify a JWT token on protected requests
#
# The SECRET_KEY is what makes tokens unforgeable.
# If someone changes the payload, the signature won't match
# and we reject the token.

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import settings


def create_access_token(user_id: int) -> str:
    """
    Create a JWT token for a given user ID.
    
    The token contains:
    - sub: the user's ID (subject)
    - exp: expiry time (when the token stops working)
    
    After expiry, the user must log in again.
    This limits damage if a token is stolen.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),  # Always store as string
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def decode_access_token(token: str) -> int | None:
    """
    Decode a JWT token and return the user_id.
    
    Returns None if:
    - Token is invalid (tampered with)
    - Token has expired
    - Token is malformed
    
    The caller (dependencies.py) handles the None case
    by raising a 401 Unauthorized error.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None