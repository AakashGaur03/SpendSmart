"""
Build training dataset from user feedback.

Input:
    data/raw/feedback.jsonl

Output:
    training/data/feedback_dataset.csv

Format:
    text,label
    uber ride to office,Transport
"""

import os
import sys
import json
import csv
from typing import List, Dict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils.text_utils import clean_text


# ---------------- Path Setup ---------------- #


FEEDBACK_DATA_DIR = os.path.join(BASE_DIR, "feedback")
FEEDBACK_FILE = os.path.join(FEEDBACK_DATA_DIR, "feedback.jsonl")

OUTPUT_DIR = os.path.join(BASE_DIR, "training", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "feedback_dataset.csv")


# ---------------- Constants ---------------- #

ALLOWED_CATEGORIES = {
    "Food",
    "Shopping",
    "Bills",
    "Transport",
    "Entertainment",
    "Personal",
    "Other"
}


# ---------------- Core Logic ---------------- #

def load_feedback() -> List[Dict]:
    if not os.path.exists(FEEDBACK_FILE):
        print("⚠️ feedback.jsonl not found — no new training data")
        return []

    records = []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    print(f"✅ Loaded {len(records)} feedback records")
    return records


def validate_record(rec: Dict) -> bool:
    return (
        bool(rec.get("item"))
        and bool(rec.get("user_selected_category"))
        and rec["user_selected_category"] in ALLOWED_CATEGORIES
    )


def build_dataset(records: List[Dict]) -> List[Dict]:
    rows = []
    seen = set()

    for rec in records:
        if not validate_record(rec):
            continue

        text = clean_text(rec["item"])
        label = rec["user_selected_category"]

        key = f"{text}|{label}"
        if key in seen:
            continue

        seen.add(key)
        rows.append({"text": text, "label": label})

    print(f"✅ Built {len(rows)} clean training rows")
    return rows


def save_csv(rows: List[Dict]):
    if not rows:
        print("⚠️ No training data generated")
        return

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"📁 Dataset saved → {OUTPUT_FILE}")


# ---------------- Entry ---------------- #

if __name__ == "__main__":
    records = load_feedback()
    dataset = build_dataset(records)
    save_csv(dataset)
