"""
statistics.py - İstatistik Araçları
====================================
Görev: Havva
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
from pandas.api.types import is_numeric_dtype

# config'den ayarları import et
from config import MAX_ROWS_FOR_ANALYSIS

def compute_statistics(context: Any, cat_th=10, car_th=20) -> Dict[str, Any]:
    """
    Veri seti için temel istatistikleri hesapla.
    
    Args:
        context: ExecutionContext objesi
            - context.dataframe: pandas DataFrame
            - cat_th: Sayisal ama kategorik değişkenler için eşik değer. 
            -    (Not: 100 satirdan küçük datasetlerde bu değerin 2-5 arasina çekilmesi önerilir.)
            - car_th: Kategorik ama yüksek kardinaliteli değişkenler için eşik değer.

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
    1. DataFrame'i al +
    2. Sayısal sütunlar için describe() çalıştır +
    3. Kategorik sütunlar için describe() çalıştır +
    4. Genel bilgileri hesapla
    5. Sonucu dict olarak döndür
    """
    try:
        df = context.dataframe
        if df is None or not isinstance(df, pd.DataFrame):
            return {"success": False, "error": "Geçerli bir DataFrame yapisi bulunamadi"}
        if df.empty:
            return {"success": False, "error": "DataFrame boş; analiz yapilamaz"}
        
        print("DataFrame analiz süreci başlatiliyor...")

        if len(df) > MAX_ROWS_FOR_ANALYSIS:
            df = df.sample(MAX_ROWS_FOR_ANALYSIS)
            print(f"Performans kisiti: Analiz için dataset {MAX_ROWS_FOR_ANALYSIS} satir ile sinirlandirildi")
        else:
            print(f"Performans kisitlaması yok. Datasetin tamamı analiz edilecek.")

        # kategorik sütunların ayrımı (object + category)
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        # nümerik ama kategorik sütunların ayrımı
        num_but_cat = [col for col in df.columns if df[col].nunique() < cat_th and
                   is_numeric_dtype(df[col])]
        # kategorik ama kardinal sütunlarına ayrımı
        cat_but_car = [col for col in df.columns if df[col].nunique() > car_th and
                   not is_numeric_dtype(df[col])]
        # kategorik sütunların birleşimi ve temizliği
        categorical_cols = categorical_cols + num_but_cat
        categorical_cols = [col for col in categorical_cols if col not in cat_but_car]

        # nümerik sütunların ayrımı
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in num_but_cat]

        # numeric istatistikler
        numeric_stats = {}
        if numeric_cols:
            desc = df[numeric_cols].describe()
            for col in numeric_cols:
                numeric_stats[col] = desc[col].to_dict()

        # kategorik istatistikler
        categorical_stats = {}
        if categorical_cols:
            for col in categorical_cols:
                categorical_stats[col] = {
                    "count": int(df[col].count()),
                    "unique": int(df[col].nunique()),
                    "top": df[col].mode().iloc[0] if not df[col].mode().empty else None,
                    "freq": int(df[col].value_counts().iloc[0]) if not df[col].value_counts().empty else 0
             }
                
        return {
            "success": True,
            "numeric_stats": numeric_stats,
            "categorical_stats": categorical_stats,
            "overall": {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "numeric_columns": len(numeric_cols),
                "categorical_columns": len(categorical_cols)
            }
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Veri inceleme sirasinda hata olustu: {str(e)}",
            "numeric_stats": {},
            "categorical_stats": {},
            "overall": {}
        }


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
