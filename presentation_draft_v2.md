# Case Study 2: Multi-Agent Yerel RAG Sistemi Sunum Taslağı

## Sayfa 1: Senaryo ve Problem Tanımı
**Başlık:** Tek Başına Yetersiz Olan LLM'lerden "Süper Güçlü" Ajanlara Geçiş

*   **Problem:** Standart Büyük Dil Modelleri (LLM), eğitim verileriyle sınırlıdır. "Güncel Bitcoin fiyatı nedir?" veya "Bu PDF'teki verilerle şu istatistiksel analizi yap" gibi karmaşık, çok adımlı veya dış dünyaya erişim gerektiren soruları tek başlarına yanıtlayamazlar. Halüsinasyon görme riskleri yüksektir.
*   **Çözüm:** **Multi-Agent (Çok Ajanlı) Mimari**.
    *   Sistemi tek bir model yerine, özelleşmiş yeteneklere (Tools) sahip "uzmanlar takımı" olarak tasarlamak.
    *   Örneğin: Bir ajan sadece internette arama yaparken, diğeri sadece Python kodu çalıştırarak hesaplama yapar.
*   **Değer:** Kullanıcı karmaşık bir soru sorduğunda, sistem arka planda bir ekip gibi çalışır, veriyi bulur, işler ve kanıtlı (grounded) bir cevap üretir.

---

## Sayfa 2: Ajan Rolleri (Uzmanlar Takımı)
**Başlık:** Otonom Ekibimizle Tanışın

Bu projede, LangGraph kullanılarak orkestra edilen, hiyerarşik bir ("Supervisor") yapı kurgulanmıştır:

1.  **Supervisor (Yönetici / Orkestra Şefi):**
    *   **Görevi:** Kullanıcıdan gelen soruyu analiz eder ve "Bu iş için hangi uzmana ihtiyacım var?" kararını verir.
    *   **Özelliği:** En hızlı yanıtı vermek için optimize edilmiş, daha küçük ve hızlı bir model (Fast Model) kullanır. İşin kendisini yapmaz, sadece delege eder.
2.  **Web Researcher (Araştırmacı - DuckDuckGo):**
    *   **Görevi:** İnternet erişimi gerektiren güncel bilgileri (borsa verileri, haberler, hava durumu) toplar.
3.  **Code Interpreter (Yazılımcı - Python REPL):**
    *   **Görevi:** Matematiksel hesaplamalar, veri analizi veya mantıksal işlem gerektiren durumlarda Python kodu yazar ve çalıştırır. LLM'lerin matematikteki zayıflığını kod çalıştırarak kapatır.
4.  **Document Expert (RAG Uzmanı - Vector DB):**
    *   **Görevi:** Kurum içi dokümanlarda (PDF, TXT) anlamsal arama yapar. Şirket hafızasına erişimi vardır.

---

## Sayfa 3: Mimari Akış
**Başlık:** LangGraph ile Stateful Orkestrasyon

Geleneksel "Chain" (Zincir) yapılarının aksine, Ajanlar "Döngüsel" ve "Durum Koruyan" (Stateful) bir yapıdadır.

**İş Akışı (Workflow):**
1.  **Kullanıcı Girdisi:** "/ask" endpoint'ine soru gelir.
2.  **Supervisor Kararı:** Yönetici, soruyu analiz eder (örn: "Hesaplama lazım"). -> **Karar: Coder Ajanı**.
3.  **Ajan Aksiyonu:** Coder ajanı Python kodunu yazar, çalıştırır ve sonucu Supervisor'a geri raporlar (örn: "Sonuç: 144").
4.  **Değerlendirme Döngüsü:** Supervisor cevabı alır. "Cevap yeterli mi?" diye bakar.
    *   *Yeterli ise:* Kullanıcıya "FINISH" sinyali ile cevabı döner.
    *   *Yetersiz ise:* Başka bir ajana yönlendirir (örn: "Şimdi de bu sonucu internetten doğrula" -> Researcher).

*Bu döngüsel yapı, tek seferde çözülemeyen problemlerin adım adım çözülmesini sağlar.*

---

## Sayfa 4: Model Seçim Stratejisi
**Başlık:** Göreve Özel Model Seçimi (Task-Specific Model Selection)

Her görev için devasa (70B+) modeller kullanmak maliyetli ve yavaştır. Bu projede **Hız/Maliyet/Performans** dengesini gözeten hibrit bir yapı kullanılmıştır.

*   **Fast Model (Routing & Simple Tasks):**
    *   **Model:** `Phi-3` veya `Gemma-2b`
    *   **Neden?** Supervisor'ın görevi sadece "Sınıflandırma" (Classification) yapmaktır. Bu işlem için devasa bir zeka gerekmez, hız (düşük latency) kritiktir. Küçük modeller bu işte çok başarılıdır.
*   **Smart Model (Reasoning & Coding):**
    *   **Model:** `Llama-3` veya `Mistral`
    *   **Neden?** Kod yazmak, karmaşık metinleri özetlemek veya mantıksal çıkarım yapmak yüksek zeka kapasitesi gerektirir. Burada en yetenekli model kullanılır.

**Sonuç:** Gereksiz kaynak tüketimi önlenir, sistemin tepki süresi kısalır ve toplam maliyet düşer.
