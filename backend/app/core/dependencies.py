# backend/app/core/dependencies.py
# PURPOSE: FastAPI dependency for protected routes.
#
# This is one of the most elegant patterns in FastAPI.
# Instead of writing auth logic in every route, we write
# it once here and any route can "depend" on it.
#
# How it works:
# 1. FastAPI sees Depends(get_current_user) in a route
# 2. Before running the route, it runs get_current_user
# 3. If it raises an exception, the route never runs
# 4. If it succeeds, it passes the user object to the route

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import decode_access_token
from app.services.user_service import get_user_by_id
from app.db.models import User

# OAuth2PasswordBearer tells FastAPI:
# "Tokens come from the /api/v1/auth/login endpoint"
# "Look for them in the Authorization: Bearer <token> header"
# This also makes the /docs page show an Authorize button
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate the current user from JWT token.
    
    This function is injected into protected routes.
    If anything goes wrong, it raises 401 Unauthorized
    and the route handler never executes.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the token to get user_id
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception

    # Fetch the actual user from database
    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    # Check account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user