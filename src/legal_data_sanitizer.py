"""
Project: Legal Data Cleaning & Anonymization Engine (Auto-Scan Version)
Module: legal_data_sanitizer.py
Description: 
    - Automatically scans 'data/raw/' for any JSON file.
    - Prevents decision leakage and anonymizes legal text.
"""

import json
import re
from pathlib import Path

class LegalDataSanitizer:
    def __init__(self, raw_dir, processed_dir):
        """
        Dizinleri ayarlar ve klasörleri kontrol eder.
        """
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        
        # Klasörleri oluştur (Yoksa)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.cities = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Konya", 
                      "Adana", "Kozan", "Bakırköy", "Alanya", "Aksaray", "Karaman"]

    def _find_input_file(self):
        """
        raw klasöründeki ilk .json dosyasını bulur.
        """
        json_files = list(self.raw_dir.glob("*.json"))
        
        if not json_files:
            return None
        
        # Alfabetik olarak ilk dosyayı döndür (Genellikle tek dosya olduğu varsayılır)
        return sorted(json_files)[0]

    def _mask_sensitive_info(self, text):
        """Regex ile anonimleştirme yapar."""
        text = re.sub(r"\d{4}/\d+\s+[E|K|k]\.", "[DOSYA_NO]", text)
        text = re.sub(r"\d{2}\.\d{2}\.\d{4}", "[TARİH]", text)
        text = re.sub(r"([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\svekili", "[KİŞİ] vekili", text)
        text = re.sub(r"(Davacı|Davalı|İhbar Olunan)\s*:\s*([A-ZÇĞİÖŞÜ\.\s]+)", r"\1 : [KİŞİ]", text)
        for city in self.cities:
            text = re.sub(city, "[YER]", text, flags=re.IGNORECASE)
        return text

    def _prevent_data_leakage(self, text):
        """Karar sonucunu (Onama/Bozma) budar."""
        cutoff_points = [
            r"\nVI\.\s+KARAR", 
            r"\nKARAR\n", 
            r"Açıklanan sebeple;", 
            r"GEREĞİ DÜŞÜNÜLDÜ",
            r"SONUÇ:"
        ]
        for point in cutoff_points:
            parts = re.split(point, text, flags=re.IGNORECASE)
            if len(parts) > 1:
                text = parts[0]
        return text

    def process_data(self):
        """Ana iş akışı."""
        input_file = self._find_input_file()
        
        if not input_file:
            print(f"[!] HATA: '{self.raw_dir}' klasöründe işlenecek JSON dosyası bulunamadı.")
            return

        print(f"[*] Dosya tespit edildi: {input_file.name}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        seen_texts = set()
        cleaned_results = []

        print(f"[*] İşlem başladı ({len(raw_data)} kayıt taranıyor...)")

        for item in raw_data:
            metin = item.get("metin", "")
            if not metin or metin.strip() in seen_texts:
                continue
            
            seen_texts.add(metin.strip())

            # Temizlik adımları
            metin = re.sub(r"Yazdır\nPDF Olarak Kaydet\n|Önceki Karar\nSonraki Karar|\"İçtihat Metni\"", "", metin)
            metin = self._prevent_data_leakage(metin)
            metin = self._mask_sensitive_info(metin)
            metin = re.sub(r'\s+', ' ', metin).strip()

            cleaned_results.append({"cleaned_text": metin})

        # Çıkış dosyası adını giriş dosyasına göre belirle (örn: ham_veriler_cleaned.json)
        output_name = f"{input_file.stem}_processed.json"
        self._save_output(cleaned_results, output_name)

    def _save_output(self, data, filename):
        output_path = self.processed_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("-" * 40)
        print(f"[+] BAŞARILI!")
        print(f"[+] Kayıt Sayısı: {len(data)}")
        print(f"[+] Çıkış Dosyası: {output_path}")
        print("-" * 40)

if __name__ == "__main__":
    # Klasör yapılandırması
    RAW_DIR = "data/raw"
    PROCESSED_DIR = "data/processed"
    
    # Başlat
    sanitizer = LegalDataSanitizer(RAW_DIR, PROCESSED_DIR)
    sanitizer.process_data()