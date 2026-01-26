import re


def clean_text(text: str) -> str:
    """
    Clean input text to match training-time preprocessing
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text) # Remove punctuation & numbers
    text = re.sub(r"\s+", " ", text).strip() # Normalize spaces
    return text
