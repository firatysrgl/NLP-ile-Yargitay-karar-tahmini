import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class YargitayBot:
    def __init__(self):
        print("🛠 ThinkPad Sniper Modu: 'kararAlani' Hedeflendi...")
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
        )
        self.wait = WebDriverWait(self.driver, 25)

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def kararlari_topla(self, aranacak_kelime="kıdem tazminatı", adet=10):
        self.driver.get("https://karararama.yargitay.gov.tr/")
        dataset = []

        try:
            # --- ARAMA SÜRECİ ---
            detayli = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'DETAYLI ARAMA')]")))
            self.js_click(detayli)
            time.sleep(2)

            hukuk_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-id='hukuk']")))
            self.js_click(hukuk_btn)
            time.sleep(1)

            dokuz = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='9. Hukuk Dairesi']")))
            self.js_click(dokuz)

            input_area = self.wait.until(EC.element_to_be_clickable((By.ID, "arananDetail")))
            input_area.send_keys(aranacak_kelime)

            search_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "detaylıAramaG")))
            self.js_click(search_btn)

            print("⏳ Sonuçlar yükleniyor...")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr[td]")))
            time.sleep(5)

            # --- VERİ KAZIMA ---
            for i in range(adet):
                try:
                    rows = self.driver.find_elements(By.XPATH, "//table//tbody/tr")
                    if i >= len(rows): break

                    self.js_click(rows[i])
                    print(f"   [{i + 1}] Karar seçildi, '{aranacak_kelime}' içeriği okunuyor...")

                    # KRİTİK: Gönderdiğin görseldeki id="kararAlani" içindeki metni bekle
                    # Metin card-body içinde olduğu için doğrudan kararAlani'nı okuyabiliriz
                    metin_elementi = self.wait.until(EC.visibility_of_element_located((By.ID, "kararAlani")))
                    time.sleep(2)  # İçeriğin tam yerleşmesi için

                    karar_metni = metin_elementi.text.strip()

                    if len(karar_metni) > 100:
                        # NLP için basit etiketleme (Geleneksel Onama/Bozma kontrolü)
                        etiket = "Onama" if "ONANMASINA" in karar_metni.upper() else "Bozma"
                        dataset.append({"metin": karar_metni, "karar": etiket})
                        print(f"   ✅ Karar {i + 1} başarıyla alındı. ({len(karar_metni)} karakter)")
                    else:
                        print(f"   ⚠️ Karar {i + 1} metni çok kısa veya boş.")

                except Exception as row_e:
                    print(f"   ⚠️ Satır {i + 1} işlenirken hata: {row_e}")
                    continue

            return dataset

        except Exception as e:
            print(f"❌ Kritik Hata: {e}")
            return []

    def close(self):
        if hasattr(self, 'driver'):
            self.driver.quit()