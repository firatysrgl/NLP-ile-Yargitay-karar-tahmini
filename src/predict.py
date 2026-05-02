import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer

def tahmin_et(metin):
    """
    Yargıtay karar metnini alır ve eğitilmiş BERT modelini kullanarak 
    'Onama' veya 'Bozma' tahmini döndürür.
    """
    
    # 1. DİNAMİK DOSYA YOLU AYARI
    # predict.py'nin bulunduğu klasörü (src) bulur
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Model klasörünün adı (Zip'ten çıkan klasör ismiyle aynı olmalı)
    model_klasor_adi = "Yargitay_Karar_Tahmin_Modeli_v1_Nihai"
    
    # Modelin ana dizinde (src'nin bir üstünde) olduğunu varsayar
    model_yolu = os.path.normpath(os.path.join(base_path, "..", model_klasor_adi))
    
    try:
        # 2. MODEL VE TOKENIZER YÜKLEME
        model = BertForSequenceClassification.from_pretrained(model_yolu)
        tokenizer = BertTokenizer.from_pretrained(model_yolu)
        
        # Modeli değerlendirme (inference) moduna al
        model.eval()
        
        # 3. METİN ÖN İŞLEME
        inputs = tokenizer(metin, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        # 4. TAHMİN ÜRETME
        with torch.no_grad():
            outputs = model(**inputs)
            raw_prediction = torch.argmax(outputs.logits, dim=-1).item()
        
        # 5. SPRINT 5 MAPPING (Düzeltme)
        # Analizler sonucu modelin 0=Bozma, 1=Onama şeklinde çalıştığı saptanmıştır.
        if raw_prediction == 0:
            return "Bozma"
        else:
            return "Onama"
            
    except Exception as e:
        return f"Hata: Model dosyası bulunamadı veya yüklenemedi. Detay: {e}"

# --- TEST BÖLÜMÜ ---
if __name__ == "__main__":
    # Örnek bir karar metni ile test edelim
    ornek_metin = "Davanın reddine dair verilen yerel mahkeme kararı usul ve yasaya uygun bulunmuştur."
    sonuc = tahmin_et(ornek_metin)
    print(f"\nTest Metni: {ornek_metin}")
    print(f"Model Tahmini: {sonuc}")