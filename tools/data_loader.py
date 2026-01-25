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
from pandas.api.types import is_numeric_dtype
from typing import Dict, Any, Optional
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# config'den ayarları import et
from config import MAX_ROWS_FOR_ANALYSIS, PREVIEW_ROWS


def load_and_inspect(context: Any, cat_th=10, car_th=20) -> Dict[str, Any]:
    """
    Veriyi yükle ve yapısını incele.
    
    Args:
        context: ExecutionContext objesi
            - context.dataframe: pandas DataFrame (zaten yüklenmiş olabilir)
            - context.file_path: CSV dosya yolu (opsiyonel)
            - cat_th: Sayisal ama kategorik değişkenler için eşik değer. 
            -    (Not: 100 satirdan küçük datasetlerde bu değerin 2-5 arasina çekilmesi önerilir.)
            - car_th: Kategorik ama yüksek kardinaliteli değişkenler için eşik değer.
    
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
    1. context.dataframe'i al +
    2. Eğer None ise hata döndür +
    3. shape, columns, dtypes bilgilerini çıkar +
    4. Sayısal ve kategorik sütunları ayır +
    5. Bellek kullanımını hesapla +
    6. İlk birkaç satırı sample olarak al + 
    7. Sonucu dict olarak döndür + 
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
     
        # Bellek kullanımı (MB)
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
         
        return {
            "success": True,
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "memory_usage": round(memory_mb, 2),
            "sample": df.head(PREVIEW_ROWS).to_dict(orient='records'),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Veri inceleme sirasinda hata olustu: {str(e)}",
            "columns": [],
            "numeric_columns": [],
            "categorical_columns": []
        }


def load_csv(file_path: str) -> Optional[pd.DataFrame]:
    """
    CSV dosyasını yükle.
    
    Args:
        file_path: CSV dosya yolu
    
    Returns:
        pandas DataFrame veya None (hata durumunda)
    
    TODO:
    1. pd.read_csv ile dosyayı oku +
    2. Hata varsa None döndür +
    3. Başarılıysa DataFrame döndür +
    """
    try:
        df = pd.read_csv(file_path)
        
        # csv boş mu
        if df.empty: 
            print(f"Uyari: {file_path} dosyasi boş!")
            return None
        
        # sütun sayısı kontrolleri
        num_of_cols = len(df.columns)
        if num_of_cols == 0:
            print(f"Uyari: {file_path} dosyasinda hiç sütun yok!")
            return None
        
        if num_of_cols == 1:
            print(f"Dikkat: {file_path} dosyasinda tek bir sütun var.")
        
        if num_of_cols > 50:
            print(f"Dikkat: {file_path} dosyasi {num_of_cols} adet sütun içeriyor. İşlem uzun sürebilir.")

        # sütun isimleri düzenleme
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

        print(f"İşlem Tamam: {file_path} yüklendi. ({len(df)} satir bulundu)")

        return df
    
    except FileNotFoundError:
        print(f" Hata: '{file_path}' yolunda bir dosya bulunamadi!")
        return None
    except Exception as e:
        print(f"Beklenmedik hata: {e}")
        return None

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
    1. Her sütun için döngü kur +
    2. Bilgileri topla +
    3. Dict olarak döndür +
    """
    result = {}

    try:
        for col in df.columns:
            col_info = {}
            col_info["dtype"] = str(df[col].dtype)
            col_info["non_null_count"] = int(df[col].count())
            col_info["null_count"] = int(df[col].isna().sum())
            col_info["unique_count"] = int(df[col].nunique())

            result[col] = col_info

    except Exception as e:
        print(f"Sütun bilgileri alınırken hata oluştu: {e}")

    return result


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

    # Test: load_csv
    print("\n--- load_csv() testi ---")
    test_file_name = "test_deneme.csv"
    pd.DataFrame({"Ad Soyad": ["Test"], "Yas": [20]}).to_csv(test_file_name, index=False)
    csv_result = load_csv(test_file_name)

    if csv_result is not None:
        print(f"Başarılı! Sütunlar temizlendi: {csv_result.columns.tolist()}")
        # Sütun isimleri 'ad_soyad' ve 'yas' olmuş mu bakıyoruz
    else:
        print("Hata: load_csv fonksiyonu None döndürdü!")

    # test_file_name test dosyasını sil
    if os.path.exists(test_file_name):
       os.remove(test_file_name)

    # Test: get_column_info
    print("\n--- get_column_info() testi ---")
    col_info_result = get_column_info(test_df)
    for col, info in col_info_result.items():
        print(f"Sütun: {col}, Bilgiler: {info}")

    