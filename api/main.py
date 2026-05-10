from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn.functional as F
from transformers import BertForSequenceClassification, BertTokenizer
import uvicorn

from models import PredictRequest, PredictResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "./yargitay_modeli_final"

LABEL_MAP = {
    0: "Onama",
    1: "Bozma",
    2: "Belirsiz"
}

CONFIDENCE_THRESHOLD = 0.50

HUKUKI_KELIMELER = [
    "mahkeme", "daire", "karar", "dava", "davacı", "davalı",
    "temyiz", "hüküm", "yargıtay", "hukuk", "kanun", "madde",
    "tazminat", "vekil", "dilekçe", "dosya", "taraf", "itiraz",
    "bozma", "onama", "ret", "kabul", "istinaf", "gerekçe",
    "mahkemesi", "kararı", "davası", "sanık", "müvekkil"
]

tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

print("=" * 40)
print(f"Model sınıf sayısı : {model.config.num_labels}")
print(f"Model id2label     : {model.config.id2label}")
print(f"LABEL_MAP          : {LABEL_MAP}")
print("=" * 40)


@app.post("/predict", response_model=PredictResponse)
async def predict_decision(request: PredictRequest):
    try:
        # 0. KONTROL: Hukuki metin mi?
        metin_lower = request.text.lower()
        if not any(kelime in metin_lower for kelime in HUKUKI_KELIMELER):
            return PredictResponse(
                durum="Belirsiz",
                mesaj="Girilen metin hukuki bir içerik taşımıyor. Lütfen Yargıtay kararı metni giriniz.",
                confidence=0.0
            )

        inputs = tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        probabilities = F.softmax(logits, dim=1)
        confidence_tensor, predicted_class_tensor = torch.max(probabilities, dim=1)

        confidence_value = float(confidence_tensor.item())
        predicted_class_id = int(predicted_class_tensor.item())

        print(f"[PREDICT] class_id={predicted_class_id} | confidence={confidence_value:.4f} | probs={probabilities.tolist()}")

        # 1. KONTROL: Güven eşiği altındaysa Belirsiz dön
        if confidence_value < CONFIDENCE_THRESHOLD:
            return PredictResponse(
                durum="Belirsiz",
                mesaj=f"Güven skoru yetersiz (%{int(confidence_value * 100)}). Lütfen metni kontrol ediniz.",
                confidence=round(confidence_value, 4)
            )

        # 2. KONTROL: Geçerli bir sınıf ID'si mi?
        if predicted_class_id not in LABEL_MAP:
            return PredictResponse(
                durum="Hata",
                mesaj=f"Model tanımsız bir sınıf döndürdü (ID: {predicted_class_id}). LABEL_MAP güncellenmeli.",
                confidence=round(confidence_value, 4)
            )

        durum_text = LABEL_MAP[predicted_class_id]

        # 3. KONTROL: Duruma göre mesaj
        mesaj_map = {
            "Onama": "Karar Onanmıştır.",
            "Bozma": "Karar Bozulmuştur.",
            "Belirsiz": "Model bu metni 'Belirsiz/Emsal Dışı' olarak kategorize etti."
        }
        mesaj_text = mesaj_map.get(durum_text, f"Bilinmeyen durum: {durum_text}")

        return PredictResponse(
            durum=durum_text,
            mesaj=mesaj_text,
            confidence=round(confidence_value, 4)
        )

    except Exception as e:
        print(f"[HATA] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)