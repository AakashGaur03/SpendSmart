from pydantic import BaseModel, Field
from typing import List, Dict

class TopPrediction(BaseModel):
    category: str
    confidence: float = Field(..., ge=0, le=1)


class FeedbackRequest(BaseModel):
    item: str = Field(..., min_length=1, description="Original expense text")

    predicted_category: str = Field(..., description="Model predicted category")

    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")

    top_predictions: List[TopPrediction]

    user_selected_category: str


class FeedbackResponse(BaseModel):
    status: str
    message: str
