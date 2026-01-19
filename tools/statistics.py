"""
statistics.py - İstatistik Araçları
====================================
Görev: Gözde
Branch: feature/tools-data-stats
Zorluk: ⭐⭐ Kolay-Orta

Bu modül temel istatistiksel hesaplamaları yapar.
pandas'ın describe() ve diğer istatistik fonksiyonlarını kullanır.

Kullanım:
    from tools.statistics import compute_statistics
    result = compute_statistics(context)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


def compute_statistics(context: Any) -> Dict[str, Any]:
    """
    Veri seti için temel istatistikleri hesapla.
    
    Args:
        context: ExecutionContext objesi
            - context.dataframe: pandas DataFrame
    
    Returns:
        dict: İstatistiksel bilgiler
            - success: bool
            - numeric_stats: sayısal sütunların istatistikleri
            - categorical_stats: kategorik sütunların istatistikleri
            - overall: genel bilgiler
    
    Örnek çıktı:
    {
        "success": True,
        "numeric_stats": {
            "Age": {
                "count": 714,
                "mean": 29.7,
                "std": 14.5,
                "min": 0.42,
                "25%": 20.125,
                "50%": 28.0,
                "75%": 38.0,
                "max": 80.0
            },
            "Fare": {...}
        },
        "categorical_stats": {
            "Sex": {
                "count": 891,
                "unique": 2,
                "top": "male",
                "freq": 577
            },
            "Embarked": {...}
        },
        "overall": {
            "total_rows": 891,
            "total_columns": 12,
            "numeric_columns": 5,
            "categorical_columns": 7
        }
    }
    
    TODO:
    1. DataFrame'i al
    2. Sayısal sütunlar için describe() çalıştır
    3. Kategorik sütunlar için describe() çalıştır
    4. Genel bilgileri hesapla
    5. Sonucu dict olarak döndür
    """
    
    # TODO: Implement this function
    
    # Örnek implementasyon başlangıcı:
    # try:
    #     df = context.dataframe
    #     
    #     if df is None:
    #         return {"success": False, "error": "DataFrame bulunamadı"}
    #     
    #     # Sayısal istatistikler
    #     numeric_df = df.select_dtypes(include=[np.number])
    #     numeric_stats = {}
    #     if not numeric_df.empty:
    #         desc = numeric_df.describe()
    #         for col in numeric_df.columns:
    #             numeric_stats[col] = desc[col].to_dict()
    #     
    #     # Kategorik istatistikler
    #     categorical_df = df.select_dtypes(include=['object', 'category'])
    #     categorical_stats = {}
    #     if not categorical_df.empty:
    #         for col in categorical_df.columns:
    #             categorical_stats[col] = {
    #                 "count": df[col].count(),
    #                 "unique": df[col].nunique(),
    #                 "top": df[col].mode().iloc[0] if not df[col].mode().empty else None,
    #                 "freq": df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
    #             }
    #     
    #     return {
    #         "success": True,
    #         "numeric_stats": numeric_stats,
    #         "categorical_stats": categorical_stats,
    #         "overall": {
    #             "total_rows": len(df),
    #             "total_columns": len(df.columns),
    #             "numeric_columns": len(numeric_df.columns),
    #             "categorical_columns": len(categorical_df.columns)
    #         }
    #     }
    # except Exception as e:
    #     return {"success": False, "error": str(e)}
    
    pass


def get_value_counts(context: Any, column: str, top_n: int = 10) -> Dict[str, Any]:
    """
    Bir sütundaki değerlerin frekanslarını hesapla.
    
    Args:
        context: ExecutionContext objesi
        column: Sütun adı
        top_n: Kaç değer gösterilecek
    
    Returns:
        dict: Değer frekansları
            - success: bool
            - column: sütun adı
            - value_counts: {değer: frekans} dict
            - total_unique: toplam benzersiz değer
    
    TODO:
    1. Sütunu kontrol et (var mı?)
    2. value_counts() çalıştır
    3. İlk top_n değeri al
    4. Sonucu döndür
    """
    # TODO: Implement this function
    pass


def get_percentiles(context: Any, column: str, 
                    percentiles: List[float] = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99]) -> Dict[str, Any]:
    """
    Bir sütun için yüzdelik dilimleri hesapla.
    
    Args:
        context: ExecutionContext objesi
        column: Sütun adı
        percentiles: Hesaplanacak yüzdelikler
    
    Returns:
        dict: Yüzdelik değerleri
    
    TODO:
    1. Sütunun sayısal olduğunu kontrol et
    2. quantile() ile yüzdelikleri hesapla
    3. Sonucu döndür
    """
    # TODO: Implement this function
    pass


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Statistics Test ===\n")
    
    # Test için DataFrame oluştur
    np.random.seed(42)
    test_df = pd.DataFrame({
        'id': range(1, 101),
        'age': np.random.normal(35, 10, 100).astype(int),
        'salary': np.random.normal(6000, 1500, 100).round(2),
        'department': np.random.choice(['IT', 'HR', 'Sales', 'Marketing'], 100),
        'city': np.random.choice(['İstanbul', 'Ankara', 'İzmir'], 100)
    })
    
    # Birkaç eksik değer ekle
    test_df.loc[5, 'age'] = np.nan
    test_df.loc[10, 'salary'] = np.nan
    
    print("Test DataFrame (ilk 5 satır):")
    print(test_df.head())
    print()
    
    # Mock context
    class MockContext:
        def __init__(self):
            self.dataframe = test_df
    
    context = MockContext()
    
    # Test: compute_statistics
    print("--- compute_statistics() testi ---")
    result = compute_statistics(context)
    
    if result is None:
        print("TODO: compute_statistics fonksiyonu henüz implement edilmedi")
        print("\nBeklenen çıktı yapısı:")
        print({
            "success": True,
            "numeric_stats": {
                "age": {"count": 99, "mean": 35.2, "std": 10.1, "...": "..."},
                "salary": {"count": 99, "mean": 6000, "...": "..."}
            },
            "categorical_stats": {
                "department": {"count": 100, "unique": 4, "top": "IT", "freq": 28},
                "city": {"count": 100, "unique": 3, "...": "..."}
            },
            "overall": {"total_rows": 100, "total_columns": 5}
        })
    else:
        print("Sonuç:")
        print(f"  Success: {result.get('success')}")
        print(f"  Numeric columns: {list(result.get('numeric_stats', {}).keys())}")
        print(f"  Categorical columns: {list(result.get('categorical_stats', {}).keys())}")
        if 'overall' in result:
            print(f"  Overall: {result['overall']}")
