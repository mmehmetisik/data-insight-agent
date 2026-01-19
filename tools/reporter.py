"""
reporter.py - Rapor Oluşturma Aracı
====================================
Görev: Kişi 2
Branch: feature/tools-analysis-reporter
Zorluk: ⭐⭐ Orta

Bu modül analiz sonuçlarından Markdown formatında rapor oluşturur.

Kullanım:
    from tools.reporter import generate_summary
    report = generate_summary(context)
"""

from typing import Dict, Any, List
from datetime import datetime


def generate_summary(context: Any) -> Dict[str, Any]:
    """
    Tüm analiz sonuçlarından özet rapor oluştur.
    
    Args:
        context: ExecutionContext objesi
            - context.dataframe: pandas DataFrame
            - context.step_results: tüm adım sonuçları
            - context.insights: önemli bulgular
    
    Returns:
        dict: Rapor bilgileri
            - success: bool
            - report_markdown: Markdown formatında rapor
            - report_html: HTML formatında rapor (opsiyonel)
            - key_findings: ana bulgular listesi
    
    Örnek çıktı:
    {
        "success": True,
        "report_markdown": "# Veri Analiz Raporu\\n\\n## Genel Bakış\\n...",
        "key_findings": [
            "Veri seti 891 satır ve 12 sütun içermektedir",
            "Age sütununda %20 eksik veri bulunmaktadır",
            "Fare ve Pclass arasında güçlü negatif korelasyon vardır"
        ]
    }
    
    TODO:
    1. context'ten tüm sonuçları al
    2. Markdown şablonunu doldur
    3. Key findings listesini oluştur
    4. Sonucu döndür
    """
    
    # TODO: Implement this function
    pass


def _create_markdown_report(context: Any) -> str:
    """
    Markdown formatında rapor oluştur.
    
    Args:
        context: ExecutionContext objesi
    
    Returns:
        str: Markdown formatında rapor
    
    Rapor yapısı:
    1. Başlık ve tarih
    2. Genel Bakış (satır/sütun sayısı, veri tipleri)
    3. Temel İstatistikler (mean, std, min, max)
    4. Veri Kalitesi (eksik veriler, outlier'lar)
    5. Korelasyonlar
    6. Sonuç ve Öneriler
    
    TODO:
    1. Her bölümü oluştur
    2. Birleştir
    3. Döndür
    """
    
    # TODO: Implement this function
    
    # Şablon örneği:
    # report = f"""
    # # 📊 Veri Analiz Raporu
    # 
    # **Oluşturma Tarihi:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
    # 
    # ---
    # 
    # ## 1. Genel Bakış
    # 
    # | Özellik | Değer |
    # |---------|-------|
    # | Satır Sayısı | {context.dataframe.shape[0]} |
    # | Sütun Sayısı | {context.dataframe.shape[1]} |
    # | Sayısal Sütunlar | {num_cols} |
    # | Kategorik Sütunlar | {cat_cols} |
    # 
    # ## 2. Temel İstatistikler
    # ...
    # 
    # ## 3. Veri Kalitesi
    # ...
    # 
    # ## 4. Korelasyonlar
    # ...
    # 
    # ## 5. Sonuç ve Öneriler
    # ...
    # """
    
    pass


def _generate_overview_section(context: Any) -> str:
    """
    Genel bakış bölümünü oluştur.
    
    TODO: Implement this function
    """
    pass


def _generate_statistics_section(context: Any) -> str:
    """
    İstatistikler bölümünü oluştur.
    
    TODO: Implement this function
    """
    pass


def _generate_quality_section(context: Any) -> str:
    """
    Veri kalitesi bölümünü oluştur.
    
    TODO: Implement this function
    """
    pass


def _generate_correlation_section(context: Any) -> str:
    """
    Korelasyon bölümünü oluştur.
    
    TODO: Implement this function
    """
    pass


def _generate_conclusion_section(context: Any) -> str:
    """
    Sonuç ve öneriler bölümünü oluştur.
    
    TODO: Implement this function
    """
    pass


def format_number(value: float, decimals: int = 2) -> str:
    """
    Sayıyı formatla.
    
    Args:
        value: Sayı
        decimals: Ondalık basamak
    
    Returns:
        str: Formatlanmış sayı
    
    Örnek:
        format_number(1234567.89) -> "1,234,567.89"
        format_number(0.12345, 3) -> "0.123"
    """
    if value is None:
        return "N/A"
    
    try:
        return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Yüzde formatla.
    
    Args:
        value: Yüzde değeri (0-100 arası)
        decimals: Ondalık basamak
    
    Returns:
        str: Formatlanmış yüzde
    
    Örnek:
        format_percentage(45.678) -> "45.7%"
    """
    if value is None:
        return "N/A"
    
    return f"{value:.{decimals}f}%"


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Reporter Test ===\n")
    
    import pandas as pd
    import numpy as np
    
    # Test DataFrame
    test_df = pd.DataFrame({
        'id': range(1, 101),
        'age': np.random.normal(35, 10, 100),
        'income': np.random.normal(50000, 15000, 100),
        'score': np.random.normal(75, 15, 100)
    })
    
    # Mock context with step results
    class MockContext:
        def __init__(self):
            self.dataframe = test_df
            self.step_results = [
                {
                    "step": "load_and_inspect",
                    "result": {"shape": (100, 4), "columns": ["id", "age", "income", "score"]}
                },
                {
                    "step": "compute_statistics",
                    "result": {"numeric_stats": {"age": {"mean": 35, "std": 10}}}
                },
                {
                    "step": "check_missing",
                    "result": {"total_missing": 5, "missing_percentage": 1.25}
                }
            ]
            self.insights = [
                "Veri setinde 100 satır bulunmaktadır",
                "Age sütununda %2 eksik veri var"
            ]
    
    context = MockContext()
    
    # Test: generate_summary
    print("--- generate_summary() testi ---")
    result = generate_summary(context)
    
    if result is None:
        print("TODO: generate_summary fonksiyonu henüz implement edilmedi")
        print("\nBeklenen rapor yapısı:")
        print("""
# 📊 Veri Analiz Raporu

**Oluşturma Tarihi:** 2025-01-19 14:30

---

## 1. Genel Bakış
| Özellik | Değer |
|---------|-------|
| Satır Sayısı | 100 |
| Sütun Sayısı | 4 |

## 2. Temel İstatistikler
...

## 3. Veri Kalitesi
...
        """)
    else:
        print("Rapor oluşturuldu!")
        print(f"Key findings: {result.get('key_findings')}")
    
    # Format fonksiyonları testi
    print("\n--- Format fonksiyonları testi ---")
    print(f"format_number(1234567.89): {format_number(1234567.89)}")
    print(f"format_percentage(45.678): {format_percentage(45.678)}")
