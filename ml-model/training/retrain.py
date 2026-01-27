# retrain.py
# │
# ├── load_base_dataset()
# ├── load_feedback_dataset()
# ├── combine_datasets()
# ├── train_vectorizer()
# ├── train_model()
# ├── evaluate_model()
# ├── save_artifacts()
# │
# └── main()


"""
Retrain expense category prediction model using:
1. Base synthetic dataset
2. Real user feedback dataset

Outputs:
    artifacts/tfidf_vectorizer.pkl
    artifacts/expense_classifier_lr.pkl
    artifacts/versions/*

Goal:
    Continually improve model using real-world feedback.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

import joblib

# ---------------- Path Setup ---------------- #

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# Data paths
BASE_DATASET_PATH = os.path.join(BASE_DIR, "data", "processed", "training_dataset.csv")
FEEDBACK_DATASET_PATH = os.path.join(BASE_DIR, "training", "data", "feedback_dataset.csv")

# Artifacts
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
VERSIONS_DIR = os.path.join(ARTIFACTS_DIR, "versions")
os.makedirs(VERSIONS_DIR, exist_ok=True)


# ---------------- Data Loaders ---------------- #

def load_base_dataset() -> pd.DataFrame:
    """
    Load base synthetic training dataset
    """
    if not os.path.exists(BASE_DATASET_PATH):
        raise FileNotFoundError(f"Base dataset not found: {BASE_DATASET_PATH}")

    df = pd.read_csv(BASE_DATASET_PATH)

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Base dataset must contain: text, label columns")

    print(f"✅ Loaded base dataset → {len(df)} rows")
    return df


def load_feedback_dataset() -> pd.DataFrame:
    """
    Load user feedback dataset (optional)
    """
    if not os.path.exists(FEEDBACK_DATASET_PATH):
        print("⚠️ No feedback dataset found — training only on base dataset")
        return pd.DataFrame(columns=["text", "label"])

    df = pd.read_csv(FEEDBACK_DATASET_PATH)

    if df.empty:
        print("⚠️ Feedback dataset empty")
        return pd.DataFrame(columns=["text", "label"])

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Feedback dataset must contain: text, label columns")

    print(f"✅ Loaded feedback dataset → {len(df)} rows")
    return df


def combine_datasets(base_df: pd.DataFrame, feedback_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge base dataset + feedback dataset
    Deduplicate ONLY feedback data
    """

    before_feedback = len(feedback_df)

    feedback_df = feedback_df.drop_duplicates(subset=["text", "label"])

    after_feedback = len(feedback_df)

    print(f"🧹 Feedback dedup → {before_feedback} → {after_feedback}")

    combined = pd.concat([base_df, feedback_df], ignore_index=True)

    print(f"🔁 Final dataset size → {len(combined)}")

    print("\n📊 Final Label Distribution:")
    print(combined["label"].value_counts())

    return combined


# ---------------- Training Pipeline ---------------- #

def split_dataset(df: pd.DataFrame):
    """
    Stratified train-test split
    """
    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print(f"Train size → {len(X_train)} | Test size → {len(X_test)}")

    return X_train, X_test, y_train, y_test


def train_vectorizer(X_train):
    """
    Train TF-IDF vectorizer
    """
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.9
    )

    X_train_vec = vectorizer.fit_transform(X_train)

    print("🧠 Vectorizer trained")

    return vectorizer, X_train_vec



def train_model(X_train_vec, y_train):
    """
    Train logistic regression classifier
    """
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train_vec, y_train)

    print("🚀 Model trained")

    return model



def evaluate(model, vectorizer, X_test, y_test):
    """
    Evaluate model performance
    """
    X_test_vec = vectorizer.transform(X_test)

    y_pred = model.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)

    print("\n📊 Evaluation Metrics:")
    print("Accuracy:", acc)
    print(classification_report(y_test, y_pred))

    return acc



def save_artifacts(model, vectorizer):
    """
    Save trained model + vectorizer
    Create versioned snapshots
    Update latest model pointer
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Create version directory
    version_dir = os.path.join(VERSIONS_DIR, timestamp)
    os.makedirs(version_dir, exist_ok=True)

    model_version_path = os.path.join(version_dir, "expense_classifier_lr.pkl")
    vec_version_path = os.path.join(version_dir, "tfidf_vectorizer.pkl")

    joblib.dump(model, model_version_path)
    joblib.dump(vectorizer, vec_version_path)

    # Update latest pointer
    latest_dir = os.path.join(ARTIFACTS_DIR, "latest")
    os.makedirs(latest_dir, exist_ok=True)

    joblib.dump(model, os.path.join(latest_dir, "expense_classifier_lr.pkl"))
    joblib.dump(vectorizer, os.path.join(latest_dir, "tfidf_vectorizer.pkl"))

    print("💾 Versioned artifacts saved")
    print(f"📦 Version snapshot → {version_dir}")
    print(f"🔥 Latest model updated → {latest_dir}")



# ---------------- Entry ---------------- #

def main():
    base_df = load_base_dataset()
    feedback_df = load_feedback_dataset()

    final_df = combine_datasets(base_df, feedback_df)

    X_train, X_test, y_train, y_test = split_dataset(final_df)

    vectorizer, X_train_vec = train_vectorizer(X_train)

    model = train_model(X_train_vec, y_train)

    evaluate(model, vectorizer, X_test, y_test)

    save_artifacts(model, vectorizer)


if __name__ == "__main__":
    main()