"""
Build base training dataset from raw transaction data.

Input:
    data/raw/primary_spending_patterns_detailed.csv

Output:
    data/processed/training_dataset.csv

Format:
    text,label
"""

import os
import sys
import pandas as pd
import re

# ---------------- Path Setup ---------------- #

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

RAW_DATA_PATH = os.path.join(
    BASE_DIR, "data", "raw", "primary_spending_patterns_detailed.csv"
)

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(PROCESSED_DIR, "training_dataset.csv")

# ---------------- Constants ---------------- #

CATEGORY_MAPPING = {
    "Groceries": "Food",
    "Food": "Food",
    "Shopping": "Shopping",
    "Subscriptions": "Bills",
    "Housing and Utilities": "Bills",
    "Transportation": "Transport",
    "Hobbies": "Entertainment",
    "Friend Activities": "Entertainment",
    "Travel": "Entertainment",
    "Personal Hygiene": "Personal",
    "Fitness": "Personal",
    "Medical/Dental": "Other",
    "Gifts": "Other",
}

ALLOWED_CATEGORIES = {
    "Food",
    "Shopping",
    "Bills",
    "Transport",
    "Entertainment",
    "Personal",
    "Other",
}

# ---------------- Text Cleaning ---------------- #

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------------- Core Logic ---------------- #

def build_base_dataset():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw dataset not found: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)

    if "Item" not in df.columns or "Category" not in df.columns:
        raise ValueError("CSV must contain Item and Category columns")

    # Normalize categories
    df["label"] = df["Category"].map(CATEGORY_MAPPING)

    # Drop invalid rows
    df = df[df["label"].isin(ALLOWED_CATEGORIES)]

    # Clean text
    df["text"] = df["Item"].astype(str).apply(clean_text)

    # Remove blanks
    df = df[(df["text"] != "") & (df["label"] != "")]

    # Keep only required columns
    df_final = df[["text", "label"]]

    # Drop duplicates
    # Removed was cutting down data to 50
    # df_final = df_final.drop_duplicates()

    df_final.to_csv(OUTPUT_FILE, index=False)
    
    # print("Total rows:", len(df))

    # print("\nCategory distribution (RAW):")
    # print(df["Category"].value_counts().head(20))

    # print("\nAfter mapping:")
    # print(df["label"].value_counts())

    # print("\nAfter filtering:", len(df_final))


    print("✅ Base dataset built successfully")
    print(f"📁 Output → {OUTPUT_FILE}")
    print(f"📊 Rows → {len(df_final)}")

# ---------------- Entry ---------------- #

if __name__ == "__main__":
    build_base_dataset()
