# Local Multi-Agent RAG Service

**Yinov AI - Multi-Agent Assistant**, yerel LLM (Ollama) ve **LangGraph** kullanarak geliştirilmiş otonom bir yapay zeka sistemidir. Bu sistem, **Web Search**, **Python Code Execution** ve **Document RAG** yeteneklerini birleştirerek karmaşık soruları çözer.

##  Proje Hakkında
Bu proje, sadece doküman okuyan bir RAG sistemi değil, aynı zamanda internete çıkabilen, kod yazabilen ve kararlar alabilen bir **Multi-Agent (Çok Ajanlı)** sistemdir. Verileriniz tamamen **yerel makinenizde** işlenir.

###  Öne Çıkan Özellikler
*   **Otonom Karar Verme (Router):** Supervisor (Yönetici), sorunun türüne göre hangi ajanı kullanacağına kendisi karar verir.
*   **Multi-Model Stratejisi (Task-Specific):**
    *   **Hızlı Model (Fast LLM):** Yönlendirme ve basit kararlar için `phi3` veya `gemma` kullanır.
    *   **Akıllı Model (Smart LLM):** Kod yazma ve karmaşık analizler için `llama3` veya `mistral` kullanır.
*   **Araç Kullanımı (Tools):**
    *   DuckDuckGo Search (İnternet Araması)
    *   Python REPL (Kod Çalıştırma & Hesaplama)
    *   Vector Store (Doküman Analizi)
*   **LangGraph Orkestrasyonu:** Döngüsel (Cyclic) grafik yapısı sayesinde ajanlar birbirleriyle haberleşerek sorunu çözene kadar çalışır.

##  Mimari

Sistem, merkezi bir **Supervisor** node ve ona bağlı uzman ("Worker") node'lardan oluşur:

1.  **Supervisor:** Kullanıcı isteğini analiz eder ve ilgili işçiye yönlendirir.
2.  **Researcher:** İnternetten güncel bilgi toplar.
3.  **Coder:** Matematiksel işlemler ve veri analizi için Python kodu yazar.
4.  **RAG Expert:** Yüklenen dokümanlar üzerinde semantik arama yapar.

##  Kurulum Adımları

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

### 1. Ön Gereksinimler
*   **Python 3.10+**: Sisteminizde Python yüklü olmalıdır.
*   **Ollama**: Yerel LLM servisi. [ollama.com](https://ollama.com) adresinden indirin.

### 2. Modelleri İndirin (Önemli!)
Bu proje **iki farklı model** kullanır. Terminalde şu komutları çalıştırın:

```bash
# Router için hızlı model
ollama pull phi3

# İşlemler için akıllı model
ollama pull llama3
```

*(Not: Farklı modeller kullanmak isterseniz `app/core/config.py` dosyasını düzenleyebilirsiniz.)*

### 3. Sanal Ortam Kurulumu
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 4. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 5. Uygulamanı Çalıştırın
Ollama servisinin arka planda çalıştığından emin olun (`ollama serve`), ardından:

```bash
uvicorn app.main:app --reload
```
Uygulamanız **http://127.0.0.1:8000** adresinde yayında olacaktır.

---
### Arayüz
<img width="2868" height="1522" alt="llm" src="https://github.com/user-attachments/assets/1a6516d7-1b6f-4d58-bf81-d96610499320" />


---
**Geliştirici:** İpek Bulgurcu

