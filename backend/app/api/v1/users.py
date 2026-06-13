# backend/app/api/v1/users.py
# PURPOSE: Protected user profile routes.
#
# Notice how get_current_user is injected via Depends().
# FastAPI runs it automatically before the route handler.
# If the token is missing or invalid, the route never runs.

from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse
from app.core.dependencies import get_current_user
from app.db.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get the currently logged in user's profile.
    
    We don't need to query the database here —
    get_current_user already fetched the user for us.
    We just return it.
    """
    return current_user