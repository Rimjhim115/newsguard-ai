# backend/app/ml/train.py
# PURPOSE: Train the fake news detection model.
#
# This script is run ONCE manually by the developer.
# It reads the CSV data, trains the model, and saves
# the artifacts to disk as .pkl files.
#
# The running web server NEVER calls this file.
# It only loads the saved .pkl files via model.py.
#
# HOW TO RUN:
#   cd backend
#   python -m app.ml.train

import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ── Paths ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
FAKE_CSV = os.path.join(ARTIFACTS_DIR, "Fake.csv")
TRUE_CSV = os.path.join(ARTIFACTS_DIR, "True.csv")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "logistic_model.pkl")


def load_data():
    """
    Load and combine Fake and True CSV files.
    Label 0 = Fake, Label 1 = Real.
    """
    print("Loading data...")

    fake_df = pd.read_csv(FAKE_CSV)
    true_df = pd.read_csv(TRUE_CSV)

    fake_df["label"] = 0  # Fake
    true_df["label"] = 1  # Real

    df = pd.concat([fake_df, true_df], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"Total samples: {len(df)}")
    print(f"Fake: {len(fake_df)}, Real: {len(true_df)}")

    return df


def prepare_text(df):
    """
    Combine title and text columns for richer features.
    If only 'text' exists, use that alone.
    
    More text = more signals for the model to learn from.
    """
    if "title" in df.columns and "text" in df.columns:
        df["content"] = df["title"] + " " + df["text"]
    elif "text" in df.columns:
        df["content"] = df["text"]
    else:
        raise ValueError("CSV must have a 'text' column")

    # Drop rows with empty content
    df = df.dropna(subset=["content"])
    return df


def train():
    """
    Full training pipeline:
    1. Load data
    2. Prepare text
    3. Split into train/test sets
    4. Fit TF-IDF vectorizer
    5. Train Logistic Regression
    6. Evaluate and print metrics
    7. Save artifacts
    """

    # Step 1 & 2
    df = load_data()
    df = prepare_text(df)

    X = df["content"]
    y = df["label"]

    # Step 3 — Split data
    # 80% for training, 20% for testing
    # random_state=42 ensures reproducible splits
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples:  {len(X_test)}")

    # Step 4 — TF-IDF Vectorizer
    # max_features=50000: use top 50,000 most important words
    # ngram_range=(1,2): use single words AND two-word phrases
    #   "not good" is more informative than "not" and "good" separately
    # stop_words='english': ignore "the", "is", "at" etc.
    print("\nFitting TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),
        stop_words="english"
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Step 5 — Train Logistic Regression
    # max_iter=1000: give it enough iterations to converge
    # C=1.0: regularization strength (prevents overfitting)
    print("Training Logistic Regression...")
    model = LogisticRegression(max_iter=1000, C=1.0)
    model.fit(X_train_tfidf, y_train)

    # Step 6 — Evaluate
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n{'='*40}")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print(f"{'='*40}")
    print("\nDetailed Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=["Fake", "Real"]
    ))

    # Step 7 — Save artifacts
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(model, MODEL_PATH)

    print(f"Vectorizer saved to: {VECTORIZER_PATH}")
    print(f"Model saved to:      {MODEL_PATH}")
    print("\nTraining complete!")


if __name__ == "__main__":
    train()