"""
analysis.py - Analiz Araçları
=============================
Görev: Kişi 2
Branch: feature/tools-analysis-reporter
Zorluk: ⭐⭐ Orta

Bu modül korelasyon, eksik veri ve outlier analizlerini yapar.

Kullanım:
    from tools.analysis import find_correlations, detect_outliers, check_missing
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

# TODO: config'den ayarları import et
# from config import CORRELATION_THRESHOLD, MISSING_DATA_WARNING_THRESHOLD, OUTLIER_IQR_MULTIPLIER
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import (
    CORRELATION_THRESHOLD,
    MISSING_DATA_WARNING_THRESHOLD,
    OUTLIER_IQR_MULTIPLIER,
)


def check_missing(context: Any) -> Dict[str, Any]:
    """
    Eksik değerleri analiz et.
    
    Args:
        context: ExecutionContext objesi
            - context.dataframe: pandas DataFrame
    
    Returns:
        dict: Eksik değer analizi
            - success: bool
            - total_missing: toplam eksik değer sayısı
            - total_cells: toplam hücre sayısı
            - missing_percentage: genel eksik yüzdesi
            - by_column: sütun bazında eksik değerler
            - warnings: uyarılar listesi
    
    Örnek çıktı:
    {
        "success": True,
        "total_missing": 866,
        "total_cells": 10692,
        "missing_percentage": 8.1,
        "by_column": {
            "Age": {"count": 177, "percentage": 19.87},
            "Cabin": {"count": 687, "percentage": 77.1},
            "Embarked": {"count": 2, "percentage": 0.22}
        },
        "warnings": [
            "Cabin sütununda %77.1 eksik veri var - bu sütun analizden çıkarılabilir",
            "Age sütununda %19.9 eksik veri var - doldurmak gerekebilir"
        ]
    }
    
    TODO:
    1. DataFrame'i al
    2. Her sütun için eksik değer say
    3. Yüzdeleri hesapla
    4. Yüksek eksik oranı için uyarı oluştur
    5. Sonucu döndür
    """
    
    
    # TODO: Implement this function
    
    # İpucu:
    # missing_per_column = df.isnull().sum()
    # missing_percentage = (missing_per_column / len(df)) * 100
    
    df = getattr(context, "dataframe", None)  # df'yi context'ten al
    if not isinstance(df, pd.DataFrame):      # df kontrolü
        return {"success": False, "error": "context.dataframe pandas DataFrame olmalı."}

    n_rows, n_cols = df.shape                 # satır/sütun sayısı
    total_cells = int(n_rows * n_cols)        # toplam hücre
    if total_cells == 0:                      # boş df koruması
        return {"success": True, "total_missing": 0, "total_cells": 0,
                "missing_percentage": 0.0, "by_column": {}, "warnings": []}

    missing_per_column = df.isnull().sum()                    # sütun bazında eksik sayıları
    missing_percentage = (missing_per_column / len(df)) * 100 # sütun bazında eksik yüzdeleri

    total_missing = int(missing_per_column.sum())             # toplam eksik
    overall_pct = round((total_missing / total_cells) * 100, 1)  # genel eksik % (8.1 gibi)

    thr = MISSING_DATA_WARNING_THRESHOLD                      # eşik (0.1 => %10)
    thr_pct = thr * 100 if 0 < thr <= 1 else float(thr)       # oran ise yüzdeye çevir

    by_column: Dict[str, Dict[str, float]] = {}               # çıktı formatı
    warnings: List[str] = []                                  # uyarı listesi

    for col in df.columns:                                    # her sütunu gez
        cnt = int(missing_per_column[col])                    # eksik sayısı
        if cnt == 0:
            continue

        pct = round(float(missing_percentage[col]), 2)        # sütun % (19.87 gibi)
        by_column[col] = {"count": cnt, "percentage": pct}

        if pct >= thr_pct:                                    # eşik üstü ise uyar
            pct_msg = round(pct, 1)                           # mesajda 77.1 gibi
            action = "bu sütun analizden çıkarılabilir" if pct >= 50 else "doldurmak gerekebilir"
            warnings.append(f"{col} sütununda %{pct_msg} eksik veri var - {action}")

    return {
        "success": True,
        "total_missing": total_missing,
        "total_cells": total_cells,
        "missing_percentage": overall_pct,
        "by_column": by_column,
        "warnings": warnings,
    }

    


def find_correlations(context: Any) -> Dict[str, Any]:
    """
    Sayısal sütunlar arasındaki korelasyonları bul.
    
    Args:
        context: ExecutionContext objesi
    
    Returns:
        dict: Korelasyon analizi
            - success: bool
            - correlation_matrix: korelasyon matrisi (dict of dict)
            - strong_correlations: güçlü korelasyonlar listesi
            - warnings: uyarılar
    
    Örnek çıktı:
    {
        "success": True,
        "correlation_matrix": {
            "Age": {"Age": 1.0, "Fare": 0.096, "Pclass": -0.369},
            "Fare": {"Age": 0.096, "Fare": 1.0, "Pclass": -0.549},
            ...
        },
        "strong_correlations": [
            {"col1": "Fare", "col2": "Pclass", "correlation": -0.549, "strength": "moderate negative"},
            {"col1": "SibSp", "col2": "Parch", "correlation": 0.414, "strength": "moderate positive"}
        ],
        "warnings": []
    }
    
    TODO:
    1. Sadece sayısal sütunları seç
    2. corr() ile korelasyon matrisini hesapla
    3. Güçlü korelasyonları (>0.5 veya <-0.5) bul
    4. Sonucu döndür
    """
    
    # TODO: Implement this function
    
    # İpucu:
    # numeric_df = df.select_dtypes(include=[np.number])
    # corr_matrix = numeric_df.corr()
    # 
    # Güçlü korelasyon bulmak için:
    # for i, col1 in enumerate(corr_matrix.columns):
    #     for col2 in corr_matrix.columns[i+1:]:
    #         corr_value = corr_matrix.loc[col1, col2]
    #         if abs(corr_value) > CORRELATION_THRESHOLD:
    #             strong_correlations.append(...)
    
    df = getattr(context, "dataframe", None)  # 1) df'yi context'ten al
    if not isinstance(df, pd.DataFrame):      # df kontrolü
        return {"success": False, "error": "context.dataframe pandas DataFrame olmalı."}

    numeric_df = df.select_dtypes(include=[np.number])  # 1) sadece sayısal sütunlar
    warnings: List[str] = []

    if numeric_df.shape[1] < 2:  # korelasyon için en az 2 sayısal sütun gerekir
        return {
            "success": True,
            "correlation_matrix": {},
            "strong_correlations": [],
            "warnings": ["Korelasyon için yeterli sayısal sütun yok."],
        }

    corr_matrix = numeric_df.corr()  # 2) corr() ile korelasyon matrisi

    thr = CORRELATION_THRESHOLD  # eşik (örn 0.5)
    strong_correlations: List[Dict[str, Any]] = []

    # 3) güçlü korelasyonları bul (ipucundaki döngü)
    for i, col1 in enumerate(corr_matrix.columns):
        for col2 in corr_matrix.columns[i + 1:]:
            corr_value = float(corr_matrix.loc[col1, col2])
            if np.isnan(corr_value):
                continue
            if abs(corr_value) > thr:
                # strength etiketini üret 
                if corr_value >= 0.8:
                    strength = "strong positive"
                elif corr_value >= thr:
                    strength = "moderate positive"
                elif corr_value <= -0.8:
                    strength = "strong negative"
                else:
                    strength = "moderate negative"

                strong_correlations.append({
                    "col1": str(col1),
                    "col2": str(col2),
                    "correlation": round(corr_value, 3),  # örnekte 3 ondalık gibi
                    "strength": strength
                })


    # 4) sonucu döndür
    return {
        "success": True,
        "correlation_matrix": corr_matrix.round(3).to_dict(),  # dict of dict
        "strong_correlations": strong_correlations,
        "warnings": warnings,
    }



def detect_outliers(context: Any) -> Dict[str, Any]:
    """
    Sayısal sütunlardaki aykırı değerleri tespit et (IQR yöntemi).
    
    Args:
        context: ExecutionContext objesi
    
    Returns:
        dict: Outlier analizi
            - success: bool
            - by_column: sütun bazında outlier bilgisi
            - total_outliers: toplam outlier sayısı
            - outlier_rows: outlier içeren satır indexleri
    
    Örnek çıktı:
    {
        "success": True,
        "by_column": {
            "Age": {
                "outlier_count": 11,
                "outlier_percentage": 1.23,
                "lower_bound": 2.5,
                "upper_bound": 54.5,
                "outlier_values": [66, 70, 74, 80]
            },
            "Fare": {
                "outlier_count": 116,
                "outlier_percentage": 13.02,
                "lower_bound": -26.7,
                "upper_bound": 65.6,
                "outlier_values": [512, 263, ...]
            }
        },
        "total_outliers": 127,
        "warnings": ["Fare sütununda %13 outlier var"]
    }
    
    IQR Yöntemi:
    - Q1 = 25. yüzdelik
    - Q3 = 75. yüzdelik
    - IQR = Q3 - Q1
    - Lower bound = Q1 - 1.5 * IQR
    - Upper bound = Q3 + 1.5 * IQR
    - Bu aralık dışındakiler outlier
    
    TODO:
    1. Sayısal sütunları seç
    2. Her sütun için IQR hesapla
    3. Outlier'ları bul
    4. Sonucu döndür
    """
    
    # TODO: Implement this function
    
    # İpucu:
    # Q1 = df[col].quantile(0.25)
    # Q3 = df[col].quantile(0.75)
    # IQR = Q3 - Q1
    # lower = Q1 - 1.5 * IQR
    # upper = Q3 + 1.5 * IQR
    # outliers = df[(df[col] < lower) | (df[col] > upper)]
    
    df = getattr(context, "dataframe", None)  # df'yi context'ten al
    if not isinstance(df, pd.DataFrame):      # df kontrolü
        return {"success": False, "error": "context.dataframe pandas DataFrame olmalı."}

    numeric_df = df.select_dtypes(include=[np.number])  # 1) sayısal sütunları seç
    if numeric_df.shape[1] == 0:
        return {
            "success": True,
            "by_column": {},
            "total_outliers": 0,
            "outlier_rows": [],
            "warnings": ["Outlier analizi için sayısal sütun bulunamadı."],
        }

    multiplier = OUTLIER_IQR_MULTIPLIER  # config dosyasına göre 1.5 kullanıldı.
    by_column: Dict[str, Any] = {}
    outlier_rows = set()
    total_outliers = 0
    warnings: List[str] = []

    for col in numeric_df.columns:
        series = numeric_df[col].dropna()  # NaN'leri dışarıda bırak
        if series.empty:
            continue

        # 2) IQR hesapla
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR

        # 3) Outlier'ları bul
        mask = (numeric_df[col] < lower) | (numeric_df[col] > upper)
        idx = df.index[mask].tolist()
        out_vals = numeric_df.loc[mask, col].dropna().unique().tolist()

        out_count = int(mask.sum())
        if out_count == 0:
            continue

        out_pct = round((out_count / len(df)) * 100, 2)

        by_column[str(col)] = {
            "outlier_count": out_count,
            "outlier_percentage": out_pct,
            "lower_bound": round(float(lower), 2),
            "upper_bound": round(float(upper), 2),
            "outlier_values": sorted(out_vals)[:20],  # listeyi çok büyütmemek için ilk 20
        }

        total_outliers += out_count
        outlier_rows.update(idx)

        # basit uyarı: %10 ve üzeri outlier varsa
        if out_pct >= 10:
            warnings.append(f"{col} sütununda %{round(out_pct, 0):.0f} outlier var")

    # 4) Sonucu döndür
    return {
        "success": True,
        "by_column": by_column,
        "total_outliers": total_outliers,
        "outlier_rows": sorted(list(outlier_rows)),
        "warnings": warnings,
    }



def _get_correlation_strength(corr: float) -> str:
    """
    Korelasyon değerine göre gücü belirle.
    
    Args:
        corr: Korelasyon değeri (-1 ile 1 arası)
    
    Returns:
        str: Korelasyon gücü açıklaması
    
    Değerler:
    - |corr| >= 0.7: strong (güçlü)
    - |corr| >= 0.5: moderate (orta)
    - |corr| >= 0.3: weak (zayıf)
    - |corr| < 0.3: negligible (önemsiz)
    """
    abs_corr = abs(corr)
    direction = "positive" if corr > 0 else "negative"
    
    if abs_corr >= 0.7:
        return f"strong {direction}"
    elif abs_corr >= 0.5:
        return f"moderate {direction}"
    elif abs_corr >= 0.3:
        return f"weak {direction}"
    else:
        return "negligible"


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Analysis Tools Test ===\n")
    
    # Test DataFrame oluştur
    np.random.seed(42)
    n = 100
    
    test_df = pd.DataFrame({
        'id': range(1, n+1),
        'age': np.random.normal(35, 10, n),
        'income': np.random.normal(50000, 15000, n),
        'score': np.random.normal(75, 15, n),
        'category': np.random.choice(['A', 'B', 'C'], n)
    })
    
    # Korelasyon oluştur (income ve score arasında)
    test_df['income'] = test_df['income'] + test_df['score'] * 100
    
    # Eksik değerler ekle
    test_df.loc[5:15, 'age'] = np.nan
    test_df.loc[20:25, 'income'] = np.nan
    
    # Outlier ekle
    test_df.loc[0, 'income'] = 500000  # Extreme outlier
    test_df.loc[1, 'age'] = 100
    
    print("Test DataFrame (ilk 5 satır):")
    print(test_df.head())
    print(f"\nShape: {test_df.shape}")
    print()
    
    # Mock context
    class MockContext:
        def __init__(self):
            self.dataframe = test_df
    
    context = MockContext()
    
    # Test: check_missing
    print("--- check_missing() testi ---")
    result = check_missing(context)
    if result is None:
        print("TODO: Henüz implement edilmedi")
    else:
        print(f"Toplam eksik: {result.get('total_missing')}")
    print()
    
    # Test: find_correlations
    print("--- find_correlations() testi ---")
    result = find_correlations(context)
    if result is None:
        print("TODO: Henüz implement edilmedi")
    else:
        print(f"Güçlü korelasyonlar: {result.get('strong_correlations')}")
    print()
    
    # Test: detect_outliers
    print("--- detect_outliers() testi ---")
    result = detect_outliers(context)
    if result is None:
        print("TODO: Henüz implement edilmedi")
    else:
        print(f"Toplam outlier: {result.get('total_outliers')}")
    
    # Correlation strength test
    print("\n--- _get_correlation_strength() testi ---")
    test_values = [0.85, 0.6, -0.4, 0.1, -0.75]
    for val in test_values:
        print(f"  {val}: {_get_correlation_strength(val)}")
