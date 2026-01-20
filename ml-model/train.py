import os
import re
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


RANDOM_STATE = 42
TEST_SIZE = 0.2
DATA_PATH = "./data/raw/primary_spending_patterns_detailed.csv"

ARTIFACTS_DIR = "./artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

category_mapping = {
    'Groceries': 'Food',
    'Food': 'Food',
    'Shopping': 'Shopping',
    'Subscriptions': 'Bills',
    'Housing and Utilities': 'Bills',
    'Transportation': 'Transport',
    'Hobbies': 'Entertainment',
    'Friend Activities': 'Entertainment',
    'Travel': 'Entertainment',
    'Personal Hygiene': 'Personal',
    'Fitness': 'Personal',
    'Medical/Dental': 'Other',
    'Gifts': 'Other',
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def train():
    # Load data
    df = pd.read_csv(DATA_PATH)

    df = df[df["Category"].isin(category_mapping)]

    # Normalize categories
    df["Normalized Category"] = df["Category"].map(category_mapping)

    # Clean text
    df["clean_item"] = df["Item"].apply(clean_text)

    X = df["clean_item"]
    y = df["Normalized Category"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # Vectorizer
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.9
    )

    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Model (FINAL CHOICE)
    model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE
    )

    model.fit(X_train_tfidf, y_train)

    # Save artifacts
    joblib.dump(vectorizer, f"{ARTIFACTS_DIR}/tfidf_vectorizer.pkl")
    joblib.dump(model, f"{ARTIFACTS_DIR}/expense_classifier_lr.pkl")

    print("✅ Training complete. Artifacts saved.")


if __name__ == "__main__":
    train()
