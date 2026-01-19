# 📊 Data Insight Agent

AI destekli otomatik veri analiz asistanı. CSV dosyalarınızı yükleyin, agent sizin için kapsamlı analiz yapsın.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Özellikler

- **Otomatik Planlama**: Agent veriye bakarak analiz planı oluşturur
- **Adım Adım Yürütme**: Her adımı görsel olarak takip edin
- **Akıllı Yorumlama**: LLM sonuçları Türkçe yorumlar
- **Kapsamlı Rapor**: Markdown formatında indirilebilir rapor
- **İnteraktif Grafikler**: Korelasyon, eksik veri, dağılım grafikleri

## 🏗️ Mimari

Bu proje **Planning + Execution** pattern'ını kullanır:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Planner   │────▶│  Executor   │────▶│  Reporter   │
│ (Plan Yap)  │     │ (Yürüt)     │     │ (Raporla)   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       │    ┌─────────────────────────┐
       └───▶│   ExecutionContext      │◀─────┘
            │   (Hafıza/State)        │
            └─────────────────────────┘
```

## 📁 Proje Yapısı

```
data-insight-agent/
├── app.py                  # Streamlit ana uygulaması
├── config.py               # Konfigürasyon
├── requirements.txt        # Bağımlılıklar
├── .env.example            # Örnek environment
│
├── agent/
│   ├── planner.py          # Plan oluşturma
│   ├── executor.py         # Plan yürütme
│   └── prompts.py          # System promptlar
│
├── tools/
│   ├── data_loader.py      # Veri yükleme
│   ├── statistics.py       # İstatistik araçları
│   ├── analysis.py         # Analiz araçları
│   └── reporter.py         # Rapor oluşturma
│
├── memory/
│   └── context.py          # Execution context
│
└── data/
    └── sample_data.csv     # Örnek veri
```

## 🚀 Kurulum

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/mmehmetisik/data-insight-agent.git
cd data-insight-agent
```

### 2. Virtual Environment Oluşturun

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. API Anahtarını Ayarlayın

```bash
cp .env.example .env
```

`.env` dosyasını açın ve Groq API anahtarınızı girin:

```
GROQ_API_KEY=your_actual_api_key_here
```

> 💡 Groq API anahtarı almak için: https://console.groq.com

### 5. Uygulamayı Çalıştırın

```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` adresine gidin.

## 📖 Kullanım

1. **Veri Yükle**: Sol panelden CSV dosyası yükleyin veya örnek veri seçin
2. **Analizi Başlat**: "🚀 Analizi Başlat" butonuna tıklayın
3. **İlerlemeyi Takip Et**: Her adımı expander'lardan inceleyin
4. **Raporu İndir**: Final raporu Markdown olarak indirin

## 👥 Ekip

| İsim | Görev | Dosyalar |
|------|-------|----------|
| **Mehmet** | Team Lead | `app.py`, `config.py`, `README.md` |
| **Gözde** | Tools - Data & Stats | `data_loader.py`, `statistics.py` |
| **Kişi 2** | Tools - Analysis | `analysis.py`, `reporter.py` |
| **Kişi 3** | Memory & Prompts | `context.py`, `prompts.py` |
| **Kişi 4** | Agent Core | `planner.py`, `executor.py` |

## 🔧 Geliştirme

### Branch Yapısı

- `main`: Kararlı sürüm (korumalı)
- `develop`: Geliştirme branch'i
- `feature/*`: Özellik branch'leri

### Commit Mesajları

```
feat: Yeni özellik eklendi
fix: Hata düzeltildi
docs: Dokümantasyon güncellendi
test: Test eklendi
```

## 📊 Örnek Çıktı

```markdown
# 📊 Veri Analiz Raporu

## 1. Genel Bakış
- Satır: 891
- Sütun: 12
- Bellek: 0.83 MB

## 2. Veri Kalitesi
⚠️ Age sütununda %20 eksik veri

## 3. Korelasyonlar
- Fare ↔ Pclass: -0.55 (moderate negative)

## 4. Sonuç
...
```

## 📚 Kaynaklar

- [Groq API Documentation](https://console.groq.com/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

**Built with ❤️ by the AI/ML Project Team**
