from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn.functional as F
# ML ekibinin belirttiği BERT sınıfları import edildi
from transformers import BertForSequenceClassification, BertTokenizer
import uvicorn
from models import PredictRequest, PredictResponse

app = FastAPI()

# CORS Ayarı (Frontend'in localhost:3000 gibi başka portlardan erişebilmesi için kritik)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ML Ekibinin ilettiği yol
MODEL_PATH = "./yargitay_modeli_final"
LABEL_MAP = {0: "Bozma", 1: "Onama"}

# ML Ekibinin ilettiği hızlı yükleme kodları
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()


@app.post("/predict", response_model=PredictResponse)
async def predict_decision(request: PredictRequest):
    try:
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True, max_length=512)

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        probabilities = F.softmax(logits, dim=1)
        confidence_tensor, predicted_class_tensor = torch.max(probabilities, dim=1)

        confidence_value = float(confidence_tensor.item())
        predicted_class_id = predicted_class_tensor.item()

        prediction_text = LABEL_MAP.get(predicted_class_id, "Bilinmiyor")

        return PredictResponse(
            prediction=prediction_text,
            confidence=confidence_value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)