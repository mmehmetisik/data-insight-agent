"""
data_loader.py - Veri Yükleme Aracı
===================================
Görev: Havva
Branch: feature/tools-data-stats
Zorluk:

Bu modül CSV dosyalarını yükler ve veri yapısını inceler.
Proje 1'deki weather.py'a benzer basit bir yapıda.

Kullanım:
    from tools.data_loader import load_and_inspect
    result = load_and_inspect(context)
"""

import pandas as pd
from typing import Dict, Any, Optional

# TODO: config'den ayarları import et
# from config import MAX_ROWS_FOR_ANALYSIS, PREVIEW_ROWS


def load_and_inspect(context: Any) -> Dict[str, Any]:
    """
    Veriyi yükle ve yapısını incele.
    
    Args:
        context: ExecutionContext objesi
            - context.dataframe: pandas DataFrame (zaten yüklenmiş olabilir)
            - context.file_path: CSV dosya yolu (opsiyonel)
    
    Returns:
        dict: Veri hakkında bilgiler
            - success: bool
            - shape: (satır, sütun) tuple
            - columns: sütun isimleri listesi
            - dtypes: sütun tipleri dict
            - memory_usage: bellek kullanımı (MB)
            - sample: ilk birkaç satır (dict formatında)
            - numeric_columns: sayısal sütunlar listesi
            - categorical_columns: kategorik sütunlar listesi
    
    Örnek çıktı:
    {
        "success": True,
        "shape": (891, 12),
        "columns": ["PassengerId", "Survived", ...],
        "dtypes": {"PassengerId": "int64", "Name": "object", ...},
        "memory_usage": 0.83,
        "sample": [{"PassengerId": 1, "Survived": 0, ...}, ...],
        "numeric_columns": ["PassengerId", "Age", "Fare"],
        "categorical_columns": ["Name", "Sex", "Embarked"]
    }
    
    TODO:
    1. context.dataframe'i al
    2. Eğer None ise hata döndür
    3. shape, columns, dtypes bilgilerini çıkar
    4. Sayısal ve kategorik sütunları ayır
    5. Bellek kullanımını hesapla
    6. İlk birkaç satırı sample olarak al
    7. Sonucu dict olarak döndür
    """
    
    # TODO: Implement this function
    
    # Örnek implementasyon başlangıcı:
    # try:
    #     df = context.dataframe
    #     
    #     if df is None:
    #         return {
    #             "success": False,
    #             "error": "DataFrame bulunamadı"
    #         }
    #     
    #     # Sayısal ve kategorik sütunları ayır
    #     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    #     categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    #     
    #     # Bellek kullanımı (MB)
    #     memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    #     
    #     return {
    #         "success": True,
    #         "shape": df.shape,
    #         "columns": df.columns.tolist(),
    #         "dtypes": df.dtypes.astype(str).to_dict(),
    #         "memory_usage": round(memory_mb, 2),
    #         "sample": df.head(5).to_dict(orient='records'),
    #         "numeric_columns": numeric_cols,
    #         "categorical_columns": categorical_cols
    #     }
    # except Exception as e:
    #     return {
    #         "success": False,
    #         "error": str(e)
    #     }
    
    pass


def load_csv(file_path: str) -> Optional[pd.DataFrame]:
    """
    CSV dosyasını yükle.
    
    Args:
        file_path: CSV dosya yolu
    
    Returns:
        pandas DataFrame veya None (hata durumunda)
    
    TODO:
    1. pd.read_csv ile dosyayı oku
    2. Hata varsa None döndür
    3. Başarılıysa DataFrame döndür
    """
    # TODO: Implement this function
    pass


def get_column_info(df: pd.DataFrame) -> Dict[str, Dict]:
    """
    Her sütun hakkında detaylı bilgi al.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        dict: Her sütun için bilgi
            - dtype: veri tipi
            - non_null_count: dolu değer sayısı
            - null_count: boş değer sayısı
            - unique_count: benzersiz değer sayısı
    
    TODO:
    1. Her sütun için döngü kur
    2. Bilgileri topla
    3. Dict olarak döndür
    """
    # TODO: Implement this function
    pass


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Data Loader Test ===\n")
    
    # Test için basit bir DataFrame oluştur
    import numpy as np
    
    test_df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Ali', 'Ayşe', 'Mehmet', 'Fatma', 'Ahmet'],
        'age': [25, 30, np.nan, 45, 28],
        'salary': [5000, 6500, 7200, np.nan, 5500],
        'city': ['İstanbul', 'Ankara', 'İzmir', 'İstanbul', 'Ankara']
    })
    
    print("Test DataFrame:")
    print(test_df)
    print()
    
    # Mock context oluştur
    class MockContext:
        def __init__(self):
            self.dataframe = test_df
    
    context = MockContext()
    
    # Test: load_and_inspect
    print("--- load_and_inspect() testi ---")
    result = load_and_inspect(context)
    
    if result is None:
        print("TODO: load_and_inspect fonksiyonu henüz implement edilmedi")
        print("\nBeklenen çıktı:")
        print({
            "success": True,
            "shape": (5, 5),
            "columns": ["id", "name", "age", "salary", "city"],
            "dtypes": {"id": "int64", "name": "object", "age": "float64", "salary": "float64", "city": "object"},
            "numeric_columns": ["id", "age", "salary"],
            "categorical_columns": ["name", "city"]
        })
    else:
        print("Sonuç:")
        for key, value in result.items():
            print(f"  {key}: {value}")
