from pydantic import BaseModel

class DecisionInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    prediction: str  # "Onama" veya "Bozma"
    confidence: float