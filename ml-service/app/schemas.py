from pydantic import BaseModel, Field
from typing import Dict

class PredictionRequest(BaseModel):
    item: str = Field(...,min_length=1,description = "Expense Item Description")

class PredictionResponse(BaseModel):
    predicted_category:str
    confidence:float
    probabilities:Dict[str,float]

# pydantic
# A library used for data validation
# Ensures API inputs/outputs follow strict rules

# BaseModel

# Parent class that gives:
# Type validation
# Automatic error messages
# JSON serialization

# Field
# Adds rules and metadata to fields

# Dict
# Python type hint
# Means: {string → float} mapping