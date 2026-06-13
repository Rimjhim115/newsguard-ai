# backend/app/ml/model.py
# PURPOSE: Load trained model and make predictions.
#
# This file is loaded ONCE when the server starts.
# The model stays in memory for fast predictions.
# Loading from disk on every request would be very slow.

import joblib
import os
from typing import Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "logistic_model.pkl")


class NewsClassifier:
    """
    Wraps the trained TF-IDF + Logistic Regression model.
    
    Loaded once at startup, reused for every prediction.
    This is the Singleton pattern applied to ML models.
    """

    def __init__(self):
        self.vectorizer = None
        self.model = None
        self._loaded = False

    def load(self):
        """Load model artifacts from disk."""
        if not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError(
                f"Vectorizer not found at {VECTORIZER_PATH}. "
                "Run train.py first."
            )
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Run train.py first."
            )

        self.vectorizer = joblib.load(VECTORIZER_PATH)
        self.model = joblib.load(MODEL_PATH)
        self._loaded = True
        print("ML model loaded successfully.")

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict whether news is REAL or FAKE.
        
        Returns:
            Tuple of (prediction, confidence)
            prediction: "REAL" or "FAKE"
            confidence: float between 0.0 and 1.0
        
        Example:
            predict("Scientists find water on Mars")
            → ("REAL", 0.87)
        """
        if not self._loaded:
            self.load()

        # Transform text using the same vectorizer used in training
        text_tfidf = self.vectorizer.transform([text])

        # Get prediction (0=Fake, 1=Real)
        prediction_label = self.model.predict(text_tfidf)[0]

        # Get probability scores for both classes
        # proba[0] = probability of Fake
        # proba[1] = probability of Real
        probabilities = self.model.predict_proba(text_tfidf)[0]
        confidence = float(max(probabilities))

        prediction = "REAL" if prediction_label == 1 else "FAKE"

        return prediction, confidence


# Single instance — imported by prediction_service.py
# Created once, reused forever
classifier = NewsClassifier()