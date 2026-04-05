from fastapi import FastAPI
from api.models import DecisionInput, PredictionOutput

app = FastAPI(title="Yargitay NLP API")

@app.get("/")
def health_check():
    return {"status": "running", "target": "9. Hukuk Dairesi"}

@app.post("/predict", response_model=PredictionOutput)
async def predict_decision(input_data: DecisionInput):
    # TODO: Buraya PyTorch modelini yükleyip (torch.load) tahmini yaptıracağız
    # Şimdilik simüle ediyoruz
    return {
        "prediction": "Bozma",
        "confidence": 0.92
    }