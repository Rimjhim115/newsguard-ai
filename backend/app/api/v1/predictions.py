# backend/app/api/v1/predictions.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services import prediction_service
from app.core.dependencies import get_current_user
from app.db.models import User

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/analyze", response_model=PredictionResponse, status_code=201)
def analyze_news(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← Protected
):
    """
    Submit news for verification.
    Now uses the real logged-in user's ID from JWT.
    """
    return prediction_service.create_prediction(
        db=db,
        request=request,
        user_id=current_user.id  # ← Real user ID, not hardcoded
    )


@router.get("/history", response_model=List[PredictionResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← Protected
):
    """
    Get prediction history for the logged in user only.
    Each user sees only their own history.
    """
    return prediction_service.get_predictions_by_user(
        db,
        user_id=current_user.id  # ← Real user ID
    )


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← Protected
):
    """Get a single prediction — only if it belongs to you."""
    prediction = prediction_service.get_prediction_by_id(db, prediction_id)

    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction not found"
        )

    # Security check: make sure this prediction belongs
    # to the requesting user — not someone else's
    if prediction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this prediction"
        )

    return prediction