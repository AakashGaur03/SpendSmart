# ML Service – Expense Category Prediction

This service exposes a lightweight API for predicting expense categories
using a pre-trained NLP model.

It **does not train models**.
It only loads trained artifacts and performs inference.

---

## Responsibilities

This service is responsible for:

- Loading trained ML artifacts (model + vectorizer)
- Cleaning incoming expense text
- Predicting expense category
- Returning:
  - predicted category
  - confidence score
  - per-category probabilities
  - confidence level (high / medium / low)

---

## Model Details

- Model: Logistic Regression (TF-IDF features)
- Input: Short expense item text (e.g. `"metro ticket"`)
- Output: One of the normalized categories:
  - Food
  - Shopping
  - Bills
  - Transport
  - Entertainment
  - Personal
  - Other

The model also provides prediction probabilities using `predict_proba`.

---

## Virtual Environment Setup

We use a Python virtual environment to isolate dependencies.

```bash
# Create venv in the project root
python3 -m venv venv
source venv/bin/activate  # Linux / Mac
# OR
venv\Scripts\activate     # Windows


pip install -r requirements.txt
uvicorn main:app --reload

```

## Project Structure

````text
ml-service/
├── artifacts/
│   ├── tfidf_vectorizer.pkl
│   └── expense_classifier_lr.pkl
├── schema.py        # Request & response schemas (Pydantic)
├── text_utils.py    # Text cleaning utilities
├── config.py        # Model & vectorizer loading
├── predictor.py    # Core prediction logic
├── main.py          # API entrypoint (FastAPI)
└── README.md

---

## What This Service Does NOT Do

- Model training
- Data preprocessing pipelines
- User feedback storage
- Retraining automation
- Database access

These responsibilities belong to other modules.

---

## Running Locally (after main.py is added)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
````
