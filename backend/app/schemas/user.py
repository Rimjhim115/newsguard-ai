# # backend/app/schemas/user.py
# # PURPOSE: Pydantic schemas for User data validation.
# #
# # We have THREE different user schemas because different
# # situations need different data:
# #
# # UserCreate  → what the client sends to register
# # UserLogin   → what the client sends to login  
# # UserResponse → what we send BACK to the client
# #               (notice: NO password field here — never expose it)

# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import Optional


# class UserCreate(BaseModel):
#     """
#     Schema for registration requests.
#     The client MUST send all three fields.
#     EmailStr automatically validates email format.
#     """
#     username: str
#     email: EmailStr
#     password: str


# class UserLogin(BaseModel):
#     """
#     Schema for login requests.
#     """
#     email: EmailStr
#     password: str


# class UserResponse(BaseModel):
#     """
#     Schema for what we return about a user.
#     NEVER includes password or hashed_password.
#     This is what the frontend sees.
#     """
#     id: int
#     username: str
#     email: str
#     is_active: bool
#     created_at: datetime

#     class Config:
#         # Tells Pydantic to read data from SQLAlchemy
#         # model attributes, not just plain dictionaries
#         from_attributes = True
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    What we return after successful login.
    
    access_token: the JWT token the client stores and sends
    token_type: always "bearer" — industry standard
    """
    access_token: str
    token_type: str = "bearer"