# backend/app/api/v1/verification.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.verification import VerificationRequest, VerificationResponse
from app.services.verification_service import verify_news
from app.services.prediction_service import create_prediction
from app.core.dependencies import get_current_user
from app.db.models import User

router = APIRouter(prefix="/verify", tags=["Verification"])


@router.post("/", response_model=VerificationResponse)
def verify_news_claim(
    request: VerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Full news verification:
    1. Run ML prediction
    2. Search DuckDuckGo for sources
    3. Analyze source credibility
    4. Return comprehensive report
    """
    # Step 1: ML prediction
    from app.ml.model import classifier
    ml_prediction, ml_confidence = classifier.predict(request.news_text)

    # Step 2: Save to database
    create_prediction(
        db=db,
        request=request,
        user_id=current_user.id
    )

    # Step 3: Full verification
    report = verify_news(
        claim=request.news_text,
        ml_prediction=ml_prediction,
        ml_confidence=ml_confidence
    )

    return report