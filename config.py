"""
config.py - Konfigürasyon Dosyası
=================================
Görev: Team Lead (Mehmet)
Durum: TAMAMLANDI ✓

Bu dosya proje genelinde kullanılan ayarları içerir.
"""

import os
from dotenv import load_dotenv

# .env dosyasından değişkenleri yükle
load_dotenv()

# =============================================================================
# API AYARLARI
# =============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =============================================================================
# MODEL AYARLARI
# =============================================================================

# Planlama için model (daha akıllı olmalı)
PLANNER_MODEL = "llama-3.1-70b-versatile"

# Yürütme için model (daha hızlı olabilir)
EXECUTOR_MODEL = "llama-3.1-70b-versatile"

# Model parametreleri
MODEL_TEMPERATURE = 0.3  # Düşük = daha tutarlı
MAX_TOKENS = 2000

# =============================================================================
# ANALİZ AYARLARI
# =============================================================================

# Maksimum analiz edilecek satır sayısı (performans için)
MAX_ROWS_FOR_ANALYSIS = 10000

# Korelasyon eşiği (bu değerin üstü "güçlü korelasyon" sayılır)
CORRELATION_THRESHOLD = 0.7

# Eksik veri uyarı eşiği (bu yüzdenin üstü uyarı verir)
MISSING_DATA_WARNING_THRESHOLD = 0.1  # %10

# Outlier tespiti için IQR çarpanı
OUTLIER_IQR_MULTIPLIER = 1.5

# =============================================================================
# UI AYARLARI
# =============================================================================

# Streamlit sayfa ayarları
PAGE_TITLE = "📊 Data Insight Agent"
PAGE_ICON = "📊"
PAGE_LAYOUT = "wide"

# Maksimum önizleme satırı
PREVIEW_ROWS = 10

# =============================================================================
# DOĞRULAMA
# =============================================================================

def validate_config():
    """Konfigürasyonu doğrula"""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY bulunamadı! .env dosyasını kontrol edin.")
    return True


# Modül yüklendiğinde otomatik doğrulama (opsiyonel)
# validate_config()
