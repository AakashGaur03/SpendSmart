# ML Service – Expense Category Prediction

This service exposes a lightweight API for predicting expense categories
using a pre-trained NLP model.

It **does not train models at runtime**.
It performs inference and **collects structured user feedback for future retraining**.

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
  - top-3 category suggestions
- Collecting structured user feedback for continuous learning

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

## Setup

### Prerequisites

1. **Copy model artifacts from ml-model:**

   ```bash
   # From project root
   cp ml-model/artifacts/latest/*.pkl ml-service/artifacts/
   ```

   Or manually copy:
   - `ml-model/artifacts/latest/expense_classifier_lr.pkl` → `ml-service/artifacts/`
   - `ml-model/artifacts/latest/tfidf_vectorizer.pkl` → `ml-service/artifacts/`

2. **Virtual Environment Setup:**

   ```bash
   # Create venv in the project root
   python3 -m venv venv
   source venv/bin/activate  # Linux / Mac
   # OR
   venv\Scripts\activate     # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Run the service:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The service will start on `http://localhost:8000`

## Project Structure

```text
ml-service/
├── app/
│   ├── main.py                # FastAPI app entrypoint
│   ├── predictor.py           # Core ML inference logic
│   ├── text_utils.py          # Text preprocessing utilities
│   ├── config.py              # Model & vectorizer loader
│   ├── schema/
│   │   ├── prediction.py      # Prediction request/response schemas
│   │   └── feedback.py        # Feedback schemas
│   ├── storage/
│   │   └── feedback_store.py  # Feedback persistence layer
│
├── artifacts/
│   ├── tfidf_vectorizer.pkl   # Trained TF-IDF vectorizer
│   └── expense_classifier_lr.pkl # Trained ML model
│
├── data/
│   └── feedback.jsonl         # Append-only feedback event store
│
├── requirements.txt
├── README.md
└── venv/
```

---

## Configuration

The service loads model artifacts from `artifacts/` directory on startup:

- `artifacts/expense_classifier_lr.pkl` - Trained Logistic Regression model
- `artifacts/tfidf_vectorizer.pkl` - TF-IDF vectorizer

Make sure these files exist before starting the service. Copy them from `ml-model/artifacts/latest/` after training.

## What This Service Does NOT Do

- Model training (handled offline in `ml-model/`)
- Automated retraining pipelines (future scope)
- Model deployment orchestration
- Database access (uses file-based feedback storage)
- User authentication/authorization

These responsibilities belong to other modules.

---

## API Endpoints

### Health Check

**GET** `/health`

Check if the service is running.

**Response:**

```json
{
	"status": "ok"
}
```

---

### Predict Expense Category

**POST** `/predict`

Predict the category for an expense item description.

**Request:**

```json
{
	"item": "metro ticket"
}
```

**Response:**

```json
{
	"predicted_category": "Transport",
	"confidence": 0.87,
	"confidence_level": "high",
	"probabilities": {
		"Food": 0.02,
		"Shopping": 0.01,
		"Bills": 0.03,
		"Transport": 0.87,
		"Entertainment": 0.04,
		"Personal": 0.02,
		"Other": 0.01
	},
	"top_predictions": [
		{
			"category": "Transport",
			"confidence": 0.87
		},
		{
			"category": "Entertainment",
			"confidence": 0.04
		},
		{
			"category": "Bills",
			"confidence": 0.03
		}
	]
}
```

**Confidence Levels:**

- `high`: confidence ≥ 0.85
- `medium`: 0.50 ≤ confidence < 0.85
- `low`: confidence < 0.50

**Error Responses:**

- `400 Bad Request`: Invalid input (empty item, etc.)
- `500 Internal Server Error`: Model loading or prediction failure

---

### Submit User Feedback

**POST** `/feedback`

Submit user feedback when they correct a prediction. This data is used for future model retraining.

**Request:**

```json
{
	"item": "uber ride to office",
	"predicted_category": "Food",
	"confidence": 0.24,
	"top_predictions": [
		{
			"category": "Food",
			"confidence": 0.24
		},
		{
			"category": "Entertainment",
			"confidence": 0.23
		},
		{
			"category": "Personal",
			"confidence": 0.15
		}
	],
	"user_selected_category": "Transport"
}
```

**Response:**

```json
{
	"status": "success",
	"message": "Feedback stored successfully"
}
```

Feedback is stored in `data/feedback.jsonl` as an append-only event log.

**Error Responses:**

- `500 Internal Server Error`: Failed to store feedback

---

## Running Locally

```bash
# Activate virtual environment
source venv/bin/activate  # Linux / Mac
# OR
venv\Scripts\activate     # Windows

# Start the service
uvicorn app.main:app --reload
```

The service runs on `http://localhost:8000` by default.
