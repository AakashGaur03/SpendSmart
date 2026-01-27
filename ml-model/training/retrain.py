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
    pass


def load_feedback_dataset() -> pd.DataFrame:
    pass


def combine_datasets(base_df: pd.DataFrame, feedback_df: pd.DataFrame) -> pd.DataFrame:
    pass


# ---------------- Training Pipeline ---------------- #

def split_dataset(df: pd.DataFrame):
    pass


def train_vectorizer(X_train):
    pass


def train_model(X_train_vec, y_train):
    pass


def evaluate(model, vectorizer, X_test, y_test):
    pass


def save_artifacts(model, vectorizer):
    pass


# ---------------- Entry ---------------- #

def main():
    pass


if __name__ == "__main__":
    main()
