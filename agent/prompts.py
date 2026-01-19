"""
prompts.py - System Prompt'lar ve Şablonlar
===========================================
Görev: Kişi 3
Branch: feature/memory-prompts
Zorluk: ⭐⭐⭐ Orta

Bu modül LLM'e gönderilecek system prompt'ları ve
mesaj şablonlarını içerir.

İpuçları:
1. Prompt'lar Türkçe olmalı (çıktılar Türkçe olsun)
2. JSON formatında çıktı istemek için örnekler verin
3. Adımları net tanımlayın
"""


# =============================================================================
# PLANNER SYSTEM PROMPT
# =============================================================================

PLANNER_SYSTEM_PROMPT = """
TODO: Bu prompt'u tamamlayın.

Sen bir veri analiz planlamacısısın. Sana verilen veri seti hakkında bilgi
verilecek ve sen bu veriyi analiz etmek için bir plan oluşturacaksın.

Kullanılabilir araçlar:
- load_and_inspect: Veriyi yükle ve yapısını incele
- compute_statistics: Temel istatistikleri hesapla (mean, std, min, max)
- check_missing: Eksik değerleri analiz et
- find_correlations: Sayısal sütunlar arası korelasyonları bul
- detect_outliers: Aykırı değerleri tespit et
- generate_summary: Tüm bulgulardan özet rapor oluştur

Kurallar:
1. Her zaman load_and_inspect ile başla
2. Her zaman generate_summary ile bitir
3. Veri tipine göre uygun adımları seç
4. Maksimum 6 adım olsun

Çıktı formatı (JSON):
{
    "plan": [
        {
            "step_number": 1,
            "action": "load_and_inspect",
            "description": "Veriyi yükle ve yapısını incele",
            "tool": "data_loader"
        },
        ...
    ]
}

TODO: Bu prompt'u geliştirin ve zenginleştirin.
Örnek veri tipleri için farklı stratejiler ekleyin.
"""


# =============================================================================
# EXECUTOR SYSTEM PROMPT
# =============================================================================

EXECUTOR_SYSTEM_PROMPT = """
TODO: Bu prompt'u tamamlayın.

Sen bir veri analiz yorumlayıcısısın. Sana bir analiz adımının sonucu
verilecek ve sen bu sonucu Türkçe olarak yorumlayacaksın.

Kurallar:
1. Yorumlar kısa ve öz olsun (2-3 cümle)
2. Önemli bulguları vurgula
3. Varsa uyarıları belirt (eksik veri, outlier vb.)
4. Teknik terimleri açıkla

Örnek yorum:
"Veri setinde 891 satır ve 12 sütun bulunmaktadır. Age sütununda %20 oranında
eksik veri tespit edilmiştir. Bu durum yaş bazlı analizlerde dikkatli
olunması gerektiğini göstermektedir."

TODO: Bu prompt'u geliştirin.
Farklı adım türleri için örnek yorumlar ekleyin.
"""


# =============================================================================
# PLAN REVISION PROMPT (OPSIYONEL)
# =============================================================================

PLAN_REVISION_PROMPT = """
TODO (Opsiyonel): Plan revizyon prompt'u

Mevcut plan yürütülürken beklenmedik bir bulgu ortaya çıktı.
Bu bulguya göre planı revize etmen gerekiyor.

Mevcut Plan:
{current_plan}

Tamamlanan Adımlar:
{completed_steps}

Yeni Bulgu:
{insight}

Revize edilmiş planı JSON formatında döndür.
"""


# =============================================================================
# MESAJ ŞABLONLARI
# =============================================================================

DATA_INFO_TEMPLATE = """
Veri Seti Bilgisi:
-----------------
Boyut: {rows} satır, {cols} sütun

Sütunlar ve Tipleri:
{columns_info}

Eksik Veri Durumu:
{missing_info}

Örnek Veriler (İlk 3 satır):
{sample_data}
"""

STEP_RESULT_TEMPLATE = """
Adım: {step_name}
İşlem: {action}

Sonuç:
{result}

Bu sonucu Türkçe olarak yorumla.
"""

SUMMARY_REQUEST_TEMPLATE = """
Aşağıdaki analiz adımlarının sonuçlarını değerlendirerek
kapsamlı bir Türkçe özet rapor oluştur.

Analiz Sonuçları:
{all_results}

Tespit Edilen Önemli Bulgular:
{insights}

Rapor şu bölümleri içermeli:
1. Genel Bakış
2. Temel İstatistikler
3. Veri Kalitesi (eksik veriler, outlier'lar)
4. Önemli Korelasyonlar
5. Sonuç ve Öneriler
"""


# =============================================================================
# YARDIMCI FONKSİYONLAR
# =============================================================================

def format_data_info(shape: tuple, columns_info: str, 
                     missing_info: str, sample_data: str) -> str:
    """
    Veri bilgisini şablona göre formatla.
    
    Args:
        shape: (satır, sütun) tuple
        columns_info: Sütun bilgileri string
        missing_info: Eksik veri bilgisi string
        sample_data: Örnek veri string
    
    Returns:
        Formatlanmış string
    
    TODO: Implement this function
    """
    # TODO: DATA_INFO_TEMPLATE'i doldur ve döndür
    pass


def format_step_result(step_name: str, action: str, result: dict) -> str:
    """
    Adım sonucunu şablona göre formatla.
    
    TODO: Implement this function
    """
    pass


def format_summary_request(all_results: list, insights: list) -> str:
    """
    Özet rapor isteğini şablona göre formatla.
    
    TODO: Implement this function
    """
    pass


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Prompts Test ===\n")
    
    print("PLANNER_SYSTEM_PROMPT uzunluğu:", len(PLANNER_SYSTEM_PROMPT), "karakter")
    print("EXECUTOR_SYSTEM_PROMPT uzunluğu:", len(EXECUTOR_SYSTEM_PROMPT), "karakter")
    
    print("\n--- PLANNER_SYSTEM_PROMPT önizleme ---")
    print(PLANNER_SYSTEM_PROMPT[:500] + "...")
    
    print("\n--- Şablon Testi ---")
    # TODO: Şablon fonksiyonlarını test et
    # test_info = format_data_info(
    #     shape=(891, 12),
    #     columns_info="PassengerId: int64, Survived: int64, ...",
    #     missing_info="Age: 177 eksik, Cabin: 687 eksik",
    #     sample_data="1, 0, 3, Braund..."
    # )
    # print(test_info)
    
    print("Prompts TODO - Henüz tam implement edilmedi")
