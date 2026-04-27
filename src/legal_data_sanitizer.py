import json
import re
from pathlib import Path

class LegalDataSanitizer:
    def __init__(self, raw_dir, processed_dir):
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        self.cities = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Konya", "Adana"]

    def _mask_sensitive_info(self, text):
        # Hassas verileri maskele
        text = re.sub(r"\d{11}", "[TC_NO]", text)
        text = re.sub(r"\d{4}/\d+\s?([E|K|k]\.|Esas|Karar)", "[DOSYA_NO]", text)
        text = re.sub(r"\b\d{1,2}[./]\d{1,2}[./]\d{4}\b", "[TARİH]", text)
        return text

    def _prevent_data_leakage(self, text):
        cutoff_points = [
            r"GEREĞİ DÜŞÜNÜLDÜ\s?:", 
            r"\bHÜKÜM\b\s?:",
            r"\bSONUÇ\b\s?:"
        ]
        earliest_cut = len(text)
        found = False
        for point in cutoff_points:
            for match in re.finditer(point, text, flags=re.IGNORECASE):
                if match.start() > len(text) * 0.3: # Metnin en az %30'u geçilmiş olmalı
                    if match.start() < earliest_cut:
                        earliest_cut = match.start()
                        found = True
        return text[:earliest_cut] if found else text

    def process_data(self):
        json_files = list(self.raw_dir.glob("*.json"))
        if not json_files:
            print("[!] HATA: JSON dosyası bulunamadı.")
            return

        for input_file in json_files:
            print(f"[*] İşleniyor: {input_file.name}")
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            cleaned_results = []
            
            # Sayaçlar
            skip_empty = 0
            skip_short = 0

            for item in raw_data:
                metin = item.get("metin", "")
                
                if not metin or len(metin.strip()) < 5:
                    skip_empty += 1
                    continue

                # 1. TEMİZLİK: Gereksiz boşlukları ve karakterleri at
                metin = re.sub(r'\s+', ' ', metin).strip()
                metin = re.sub(r"Yazdır\nPDF Olarak Kaydet\n|Önceki Karar\nSonraki Karar|\"İçtihat Metni\"", "", metin)

                # 2. İŞLEM: Leakage ve Anonimleştirme
                processed_metin = self._prevent_data_leakage(metin)
                processed_metin = self._mask_sensitive_info(processed_metin)
                processed_metin = processed_metin.strip()

                # 3. KAYIT: Eğer metin hala anlamlı bir uzunluktaysa ekle
                if len(processed_metin) > 15:
                    cleaned_results.append({"cleaned_text": processed_metin})
                else:
                    skip_short += 1

            # Kaydet
            output_name = f"{input_file.stem}_processed.json"
            self._save_output(cleaned_results, output_name)
            
            print(f"--- {input_file.name} Raporu ---")
            print(f"Toplam Girdi: {len(raw_data)}")
            print(f"Başarıyla Kaydedilen: {len(cleaned_results)}")
            print(f"Atlanan (Boş/Geçersiz): {skip_empty}")
            print(f"Atlanan (Çok Kısa): {skip_short}")
            print("-" * 30)

    def _save_output(self, data, filename):
        output_path = self.processed_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    sanitizer = LegalDataSanitizer("data/raw", "data/processed")
    sanitizer.process_data()