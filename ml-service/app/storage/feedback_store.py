import os
import json
from datetime import datetime

# Base project directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# Feedback file path
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.jsonl")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


def store_feedback(feedback: dict):
    """
    Append user feedback as a JSON line for future retraining.

    Each line = one feedback event
    """
    feedback["timestamp"] = datetime.utcnow().isoformat()

    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(feedback) + "\n")
