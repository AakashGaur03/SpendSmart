# Define artifact paths (vectorizer, model)
# Load them once
# Make them reusable across the app

import os
import joblib

# __file__ current File means config.py
# abspath full absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARTIFACTS_DIR = os.path.join(BASE_DIR,"artifacts")

VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "expense_classifier_lr.pkl")

def load_vectorizer():
    return joblib.load(VECTORIZER_PATH)

def load_model():
    return joblib.load(MODEL_PATH)

vectorizer = load_vectorizer()
model = load_model()