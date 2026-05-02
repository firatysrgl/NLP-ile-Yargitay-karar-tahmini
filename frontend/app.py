import streamlit as st
import requests
import json

# Sayfa temel ayarları
st.set_page_config(page_title="YKTS | Yargıtay Karar Tahmini", page_icon="⚖️", layout="centered")

# --- RESMİ VE KURUMSAL GÖRÜNÜM İÇİN ÖZEL CSS ---
custom_css = """
<style>
/* Arka plan: Daha koyu, resmi ve kurumsal bir gri tonu (Slate) */
[data-testid="stAppViewContainer"] {
    background-color: #cbd5e1;
}

/* Üst şerit şeffaf */
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

/* BAŞLIK AYARI: "Sistemi" kelimesinin alta düşmesini engeller ve tek satıra sığdırır */
h1 {
    font-size: 2.2rem !important;
    white-space: nowrap !important;
    color: #0f172a !important; 
}

/* Tüm metinlerin rengini koyu lacivert yapar */
h2, h3, p, label, .stMarkdown {
    color: #1e293b !important; 
}

/* METİN KUTUSU: Daha köşeli, ciddi bir görünüm */
.stTextArea textarea {
    border-radius: 4px !important;
    border: 1px solid #94a3b8 !important;
    background-color: #f8fafc !important; 
    color: #0f172a !important; 
    caret-color: #0f172a !important; 
    padding: 15px !important;
}

/* Tıklandığında placeholder yazısını yok eder */
.stTextArea textarea:focus::placeholder {
    color: transparent !important;
}

/* Placeholder rengi */
.stTextArea textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* BUTON TASARIMI: Kırmızı yerine Resmi Koyu Lacivert */
.stButton button {
    background-color: #1e293b !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.5rem 1rem !important;
}

/* Buton içindeki yazıyı zorla BEYAZ ve KALIN yapar */
.stButton button, .stButton button p, .stButton button div {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Butonun üzerine gelince hafif açılan renk */
.stButton button:hover {
    background-color: #334155 !important;
}
.stButton button:hover, .stButton button:hover p, .stButton button:hover div {
    color: #ffffff !important;
}

/* SONUÇ EKRANI (Bozma/Onama) */
[data-testid="stMetricValue"] div {
    color: #0f172a !important; 
    font-weight: 800 !important;
    font-size: 2.5rem !important;
}

[data-testid="stMetricLabel"] p {
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# ---------------------------------------------------------

# Backend API URL'si
API_URL = "http://localhost:8000/predict" 

st.title("⚖️ YKTS - Yargıtay Karar Tahmin Sistemi")
st.markdown("Dokuzuncu Hukuk Dairesi dava metnini girerek **YKTS** analizini başlatabilirsiniz.")

# Kullanıcıdan dava metnini alma
dava_metni = st.text_area(
    "Dava Dosyası Metni:", 
    height=300, 
    placeholder="Karar metnini buraya yapıştırın ve analizi başlatın..."
)

# Tahmin Butonu
if st.button("Kararı Tahmin Et", type="primary"):
    if not dava_metni.strip():
        st.warning("Lütfen tahmin yapılması için bir dava metni girin.")
    else:
        with st.spinner("YKTS metni analiz ediyor..."):
            payload = {"text": dava_metni}
            
            try:
                # Backend API'sine bağlanma ve tahmin alma
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    sonuc = response.json()
                    tahmin = sonuc.get("prediction", "Bilinmiyor")
                    
                    st.success("YKTS Analizi Tamamlandı!")
                    st.metric(label="Tahmin Edilen Karar", value=tahmin)
                else:
                    st.error(f"API Hatası: {response.status_code} - Sunucu yanıt veremedi.")
            
            except requests.exceptions.ConnectionError:
                # BACKEND HAZIR OLMADIĞI AN BU KISIM ÇALIŞACAK (MOCK VERİ)
                st.warning("⚠️ Backend API'sine şu an ulaşılamıyor. YKTS sahte (mock) sonuç gösteriyor.")
                st.success("YKTS Analizi Tamamlandı! (Mock Veri)")
                
                # Sahte sonuç ekranı
                st.metric(label="Tahmin Edilen Karar", value="Bozma")