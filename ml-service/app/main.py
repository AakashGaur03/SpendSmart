from fastapi import FastAPI, HTTPException
from app.schema.prediction import PredictionRequest, PredictionResponse
from app.predictor import predict_category

from app.schema.feedback import FeedbackRequest, FeedbackResponse
from app.storage.feedback_store import store_feedback


app = FastAPI(
    title="Expense Category Prediction Service",
    description="Predicts expense categories using a trained NLP model",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring & deployment
    """
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict_expense(request: PredictionRequest):
    """
    Predict expense category from item description
    """
    try:
        result = predict_category(request.item)
        return result
    except ValueError as e:
        # Input validation errors
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Unexpected failures (model load, vectorizer, etc.)
        raise HTTPException(
            status_code=500,
            detail="Internal prediction error"
        )

@app.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest):
    """
    Store user feedback for future model retraining
    """
    try:
        store_feedback(request.dict())

        return {
            "status": "success",
            "message": "Feedback stored successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to store feedback"
        )
