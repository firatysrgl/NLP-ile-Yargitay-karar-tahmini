# ⚖️ Doğal Dil İşleme Tabanlı Yargıtay Kararı Tahmin Sistemi

Bu proje, Yargıtay 9. Hukuk Dairesi'ne ait iş davası metinlerini analiz ederek kararın **"Onama"** veya **"Bozma"** olacağını yüksek doğrulukla tahmin eden, yapay zeka destekli bir karar destek asistanıdır.

## 🎯 Projenin Amacı ve Kapsamı
Mahkemelerdeki dosya yükünü hafifletmek ve hukukçulara emsal karar araştırmalarında zaman kazandırmak amaçlanmıştır. Modelin kavram karmaşası yaşamaması ve öğrenme sürecinin optimize edilmesi amacıyla proje sadece **iş davaları (9. Hukuk Dairesi)** ile sınırlandırılmıştır.

## 👥 Geliştirici Ekip ve Görev Dağılımı
Projemiz disiplinler arası bir yaklaşımla, ayrık mimari (decoupled architecture) prensiplerine göre geliştirilmektedir:

* **Emre Eren Kızıldağ:** Veri Mühendisi & Backend Geliştirici (Veri Toplama, FastAPI Altyapısı)
* **Ali Emir Kürklü:** NLP Uzmanı & Metin Analisti (Veri Temizleme, Veri Sızıntısı Önleme, Vektörizasyon)
* **Meral Yavuztürk:** Derin Öğrenme Mühendisi (Model Eğitimi, BERTurk Fine-Tuning, Optimizasyon)
* **Fırat Yunus Yaşaroğlu:** Scrum Master & Frontend Geliştirici (Streamlit Arayüzü, API Entegrasyonu, Dokümantasyon)

## 🛠️ Kullanılan Teknolojiler (Tech Stack)
Sistemimiz baştan uca uyumluluk sağlaması amacıyla **%100 Python Ekosistemi** üzerine inşa edilmiştir.

* **Arayüz (Frontend):** Python, Streamlit, Requests
* **Sunucu (Backend):** Python, FastAPI, Uvicorn
* **Derin Öğrenme (Model):** Hugging Face (Transformers/BERTurk), PyTorch, Scikit-Learn
* **Veri Ön İşleme (NLP):** Pandas, NumPy, Regex, Zemberek/NLTK
* **Proje Yönetimi:** GitHub Projects (Agile/Scrum)

## ⚙️ Sistem Mimarisi Nasıl Çalışır?
1. Kullanıcı, `Streamlit` arayüzü üzerinden dava metnini sisteme girer.
2. Arayüz, bu metni `FastAPI` ile çalışan arka uç sunucusuna HTTP isteği olarak gönderir.
3. Sunucu, metni önceden eğitilmiş `Transformer` tabanlı modele sokar.
4. Model analizini tamamlar ve tahmin sonucunu (Onama/Bozma) JSON formatında sunucuya iletir.
5. Sunucu bu sonucu arayüze döndürür ve kullanıcı ekranda kararı görür.

---
*Bu proje akademik bir bitirme projesi kapsamında geliştirilmektedir.*
