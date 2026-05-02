\# 🏃 Sprint 2: Ürün İş Listesi (Backlog) ve Sistem Gereksinimleri



Bu doküman, NLP Yargıtay Karar Tahmin Sistemi'nin Sprint 2 kapsamındaki kullanıcı hikayelerini (User Stories), kabul kriterlerini (AC) ve fonksiyonel olmayan gereksinimlerini (NFR) içermektedir.



\## 📖 1. Kullanıcı Hikayeleri (User Stories) ve Kabul Kriterleri



\*\*Story 1: Temel Tahmin İşlevi (Hakim)\*\*

\* \*\*Hikaye:\*\* Bir hakim olarak, sistemin arayüzüne 9. Hukuk Dairesi'ne ait bir dava metnini yapıştırıp analiz butonuna basmak istiyorum; böylece davanın "Onama" mı yoksa "Bozma" mı ile sonuçlanacağını önceden görebilirim.

\* \*\*Kabul Kriteri (AC):\*\* Arayüzde geniş bir metin giriş kutusu bulunmalı ve "Tahmin Et" butonuna basıldığında sonuç ekranda açıkça gösterilmelidir.



\*\*Story 2: Olasılık Gösterimi (Avukat)\*\*

\* \*\*Hikaye:\*\* Bir avukat olarak, çıkan tahminin yanında modelin bu tahminden yüzde kaç emin olduğunu görmek istiyorum; böylece müvekkilime daha istatistiksel bir oran sunabilirim.

\* \*\*Kabul Kriteri (AC):\*\* Sonuç ekranında tahmin edilen sınıfın yanında "%85 Onama İhtimali" gibi bir güven skoru (confidence score) yer almalıdır.



\*\*Story 3: Hatalı Kullanım Engeli (Boş Metin)\*\*

\* \*\*Hikaye:\*\* Sisteme yanlışlıkla boş bir metin gönderdiğimde uyarılmak istiyorum; böylece sistemin boş yere çalışmasını veya çökmesini engellemiş olurum.

\* \*\*Kabul Kriteri (AC):\*\* Metin kutusu boşken butona basılırsa, sistem "Lütfen bir dava metni giriniz" uyarısı vermeli ve arka plana (API) istek atmamalıdır.



\*\*Story 4: Metin Temizleme Kolaylığı\*\*

\* \*\*Hikaye:\*\* Bir davayı analiz ettikten sonra arayüzdeki metni tek tuşla silmek istiyorum; böylece yeni bir dava metnini kolayca yapıştırabilirim.

\* \*\*Kabul Kriteri (AC):\*\* Arayüzde, metin kutusunun içini tamamen temizleyen bir "Yeni Sorgu" butonu bulunmalıdır.



\*\*Story 5: Model Başarısını Görme (Şeffaflık)\*\*

\* \*\*Hikaye:\*\* Sistemi kullanan biri olarak, bu yapay zekanın genel doğruluk oranını ana ekranda görmek istiyorum; böylece kullandığım sistemin ne kadar güvenilir olduğunu bilirim.

\* \*\*Kabul Kriteri (AC):\*\* Arayüzün alt kısmında veya bilgi köşesinde modelin genel test başarısı (Örn: "Doğruluk Oranı: %82") statik olarak yer almalıdır.



\*\*Story 6: API Bağlantı Kontrolü (Geliştirici/Test)\*\*

\* \*\*Hikaye:\*\* Bir geliştirici olarak, arayüzün arka plandaki yapay zeka modeline (FastAPI) doğru bağlanıp bağlanmadığını görmek istiyorum; böylece sistemin ayakta olduğundan emin olabilirim.

\* \*\*Kabul Kriteri (AC):\*\* Sistem ilk açıldığında arka planda bir "health check" yapılmalı, API'ye ulaşılamıyorsa ekranda "Sunucu Bağlantı Hatası" yazmalıdır.



\---



\## ⚙️ 2. Fonksiyonel Olmayan Gereksinimler (NFRs)



\* \*\*Performans Gereksinimi (Hız):\*\* Sistem, kullanıcı tarafından girilen dava metnini analiz edip tahmin sonucunu yerel sunucu (localhost) üzerinde maksimum \*\*5 saniye\*\* içerisinde ekrana yansıtmak zorundadır.

\* \*\*Güvenlik ve Gizlilik Gereksinimi:\*\* Sisteme yüklenen Yargıtay dava metinleri hiçbir şekilde dış bir veritabanına veya bulut ortamına kaydedilmemelidir. Veri sızıntısını önlemek için tüm süreç kapalı devre (yerel makinede) çalışmalıdır.

\* \*\*Kullanılabilirlik Gereksinimi:\*\* Sistemin web arayüzü, teknik bir altyapıya sahip olmayan hukuk profesyonellerinin (Hakim/Avukat) hiçbir eğitime ihtiyaç duymadan kullanabileceği sadelikte (minimalist) tasarlanmalıdır.

