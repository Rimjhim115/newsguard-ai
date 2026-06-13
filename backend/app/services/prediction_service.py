# backend/app/services/prediction_service.py
from sqlalchemy.orm import Session
from app.db.models import Prediction
from app.schemas.prediction import PredictionRequest
from app.ml.model import classifier


def create_prediction(
    db: Session,
    request: PredictionRequest,
    user_id: int
):
    """
    Run real ML prediction and save to database.
    Replaces the placeholder from Phase 3.
    """
    # Real ML prediction now
    prediction_label, confidence = classifier.predict(request.news_text)

    db_prediction = Prediction(
        user_id=user_id,
        news_text=request.news_text,
        prediction=prediction_label,
        confidence=confidence
    )

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return db_prediction


def get_predictions_by_user(db: Session, user_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )


def get_prediction_by_id(db: Session, prediction_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )