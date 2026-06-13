# backend/app/db/models.py
# PURPOSE: Defines database tables as Python classes.
# This is the single source of truth for your database schema.
# SQLAlchemy reads these classes and creates the actual
# MySQL tables from them.

from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, Float, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    """
    Represents the 'users' table in MySQL.
    
    Every user who registers gets one row here.
    The 'predictions' relationship lets us do:
        user.predictions  →  list of all their predictions
    without writing any SQL.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship — not a column, but tells SQLAlchemy how
    # User connects to Prediction
    # back_populates creates the reverse link on Prediction side
    predictions = relationship("Prediction", back_populates="owner")


class Prediction(Base):
    """
    Represents the 'predictions' table in MySQL.
    
    Every news verification attempt gets one row here.
    Linked to the user who made the request via user_id.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # ForeignKey enforces the relationship at the database level
    # If user id=5 is deleted, their predictions don't become orphans
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    news_text = Column(Text, nullable=False)
    prediction = Column(String(10), nullable=False)   # "REAL" or "FAKE"
    confidence = Column(Float, nullable=False)         # e.g. 0.94
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Reverse side of the relationship
    # This lets us do: prediction.owner → the User object
    owner = relationship("User", back_populates="predictions")