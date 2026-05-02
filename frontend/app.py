import streamlit as st
import requests
import json

# Backend API URL'sini belirliyoruz (Backend bitince bu adres güncellenebilir)
API_URL = "http://localhost:8000/predict" 

# Sayfa temel ayarları
st.set_page_config(page_title="Yargıtay Karar Tahmini", page_icon="⚖️", layout="centered")

st.title("⚖️ Yargıtay Karar Tahmin Sistemi")
st.markdown("Dokuzuncu Hukuk Dairesi dava dosyası metnini aşağıya girerek **YKTS** tahminini alabilirsiniz.")

# Kullanıcıdan dava metnini alma
dava_metni = st.text_area("Dava Dosyası Metni:", height=300, placeholder="Karar metnini buraya yapıştırın...")

# Tahmin Butonu
if st.button("Kararı Tahmin Et", type="primary"):
    if not dava_metni.strip():
        st.warning("Lütfen tahmin yapılması için bir dava metni girin.")
    else:
        with st.spinner("YKTS metni analiz ediyor..."):
            # Backend'e gönderilecek veri formatı (JSON)
            payload = {"text": dava_metni}
            
            try:
                # Backend API'sine bağlanmayı deniyoruz
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    sonuc = response.json()
                    tahmin = sonuc.get("prediction", "Bilinmiyor")
                    guven_skoru = sonuc.get("confidence", 0.0)
                    
                    st.success("Analiz Tamamlandı!")
                    st.metric(label="Tahmin Edilen Karar", value=tahmin)
                    st.progress(guven_skoru, text=f"Modelin Karara Güven Skoru: %{guven_skoru*100:.2f}")
                else:
                    st.error(f"API Hatası: {response.status_code} - Sunucu yanıt veremedi.")
            
            except requests.exceptions.ConnectionError:
                # BACKEND HAZIR OLMADIĞI İÇİN ŞU AN BU KISIM ÇALIŞACAK (MOCK VERİ)
                st.warning("⚠️ Backend API'sine şu an ulaşılamıyor. Arayüz testi için sahte (mock) sonuç gösteriliyor.")
                st.success("Analiz Tamamlandı! (Mock Veri)")
                
                # Sahte sonuç ekranı
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Tahmin Edilen Karar", value="Bozma")
                with col2:
                    st.metric(label="Model Güveni", value="%88.00")
                
                st.progress(0.88, text="Güven Skoru Göstergesi")