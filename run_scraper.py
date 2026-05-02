import os
import json
import sys

# Proje klasörünü yola ekleyelim
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraping.scraper import YargitayBot


def main():
    print("🚀 Yargıtay Veri Kazıma Operasyonu Başladı!")

    bot = YargitayBot()
    try:
        # Arama kelimesini ve çekilecek karar sayısını buradan ayarla
        aranacak = "kıdem tazminatı"
        karar_sayisi = 10

        veriler = bot.kararlari_topla(aranacak_kelime=aranacak, adet=karar_sayisi)

        if veriler:
            # Veriyi kaydetmek için 'data' klasörü oluştur
            os.makedirs("data", exist_ok=True)

            dosya_yolu = "data/ham_veriler.json"
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                json.dump(veriler, f, ensure_ascii=False, indent=4)

            print("-" * 30)
            print(f"✅ OPERASYON BAŞARILI!")
            print(f"📊 Toplanan Karar: {len(veriler)}")
            print(f"📂 Kayıt Yeri: {dosya_yolu}")
            print("-" * 30)
        else:
            print("❌ Maalesef hiç veri toplanamadı. Logları kontrol et.")

    except Exception as e:
        print(f"💥 Ana programda beklenmedik hata: {e}")
    finally:
        bot.close()
        print("👋 Bot kapatıldı. İyi çalışmalar Emre!")


if __name__ == "__main__":
    main()