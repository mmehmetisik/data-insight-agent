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
   

    
    # TODO 1: context'ten tüm sonuçları al
    df = getattr(context, "dataframe", None)
    if df is None:  # Neden: df yoksa rapor üretilemez.
        return {"success": False, "error": "context.dataframe bulunamadı."}

    insights = getattr(context, "insights", []) or []
    n_rows, n_cols = df.shape

    # TODO 2: Markdown şablonunu doldur
    report_md = _create_markdown_report(context)

    # TODO 3: Key findings listesini oluştur
    # Neden: missing/correlation zaten raporda var; burada tekrar etmiyoruz.
    key_findings: List[str] = [f"Veri seti {n_rows} satır ve {n_cols} sütun içermektedir"]
    if isinstance(insights, list) and insights:
        key_findings.extend([str(x) for x in insights[:5]])

    # Tekrarları temizleyip en fazla 10 madde tutuyoruz.
    seen = set()
    clean_findings: List[str] = []
    for item in key_findings:
        item = str(item).strip()
        if item and item not in seen:
            seen.add(item)
            clean_findings.append(item)
        if len(clean_findings) >= 10:
            break

    # TODO 4: Sonucu döndür
    return {
        "success": True,
        "report_markdown": report_md,
        "report_html": None,  # Neden: opsiyonel; ödevde şart değil.
        "key_findings": clean_findings,
    }





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
    
    
    # TODO 1: Her bölümü oluştur
    df = getattr(context, "dataframe", None)
    if df is None:  # Neden: df yoksa rapor üretilemez.
        return "# 📊 Veri Analiz Raporu\n\nVeri bulunamadı.\n"

    # şablondaki sayısal/kategorik sütun sayısı gösterildi.
    num_cols = len(df.select_dtypes(include="number").columns)
    cat_cols = len(df.select_dtypes(exclude="number").columns)

    # bölüm detayları ayrı fonksiyonlarda; burada sadece çağırılıp yerleştirildi.
    overview_details = _generate_overview_section(context)
    stats_details = _generate_statistics_section(context)
    quality_details = _generate_quality_section(context)
    corr_details = _generate_correlation_section(context)
    conclusion_details = _generate_conclusion_section(context)

    # TODO 2: Birleştir (Şablon örneğine göre)
    report = f"""
#  Veri Analiz Raporu

**Oluşturma Tarihi:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 1. Genel Bakış

| Özellik | Değer |
|---------|-------|
| Satır Sayısı | {df.shape[0]} |
| Sütun Sayısı | {df.shape[1]} |
| Sayısal Sütunlar | {num_cols} |
| Kategorik Sütunlar | {cat_cols} |

{overview_details}

## 2. Temel İstatistikler

{stats_details}

## 3. Veri Kalitesi

{quality_details}

## 4. Korelasyonlar

{corr_details}

## 5. Sonuç ve Öneriler

{conclusion_details}
"""

    # TODO 3: Döndür
    return report.strip()



def _generate_overview_section(context: Any) -> str:
    """
    Genel bakış bölümünü oluştur.
    
    TODO: Implement this function
    """

    df = getattr(context, "dataframe", None)  # context içinden df'yi güvenli al
    if df is None:  # df yoksa bölüm üretme
        return "## 1. Genel Bakış\n\nVeri bulunamadı.\n"

    n_rows, n_cols = df.shape  # satır/sütun sayısı
    num_cols = df.select_dtypes(include="number").columns.tolist()  # sayısal sütunlar
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()  # kategorik/diğer sütunlar

    # rapor tablosu (şablona uygun hazırlandı)
    lines = []
    lines.append("## 1. Genel Bakış")  # bölüm başlığı
    lines.append("")
    lines.append("| Özellik | Değer |")  # tablo başlıkları
    lines.append("|---------|-------|")
    lines.append(f"| Satır Sayısı | {n_rows} |")
    lines.append(f"| Sütun Sayısı | {n_cols} |")
    lines.append(f"| Sayısal Sütunlar | {len(num_cols)} |")
    lines.append(f"| Kategorik Sütunlar | {len(cat_cols)} |")
    lines.append("")

    # veri tipleri özet (çok uzamasın diye ilk 10 sütun)
    lines.append("**Veri Tipleri (ilk 10 sütun):**")  # kısa dtype listesi
    for col in df.columns[:10]:
        lines.append(f"- `{col}`: {df[col].dtype}")  # sütun tipi
    lines.append("")

    return "\n".join(lines).strip()  # tek string döndür


def _generate_statistics_section(context: Any) -> str:
    """
    İstatistikler bölümünü oluştur.
    
    TODO: Implement this function
    """
    
    df = getattr(context, "dataframe", None)
    if df is None:  #  veri yoksa istatistik üretilemez.
        return "## 2. Temel İstatistikler\n\nVeri bulunamadı.\n"

    num_df = df.select_dtypes(include="number")
    if num_df.empty:
        return "## 2. Temel İstatistikler\n\n- Sayısal sütun bulunamadı.\n"

    desc = num_df.describe().T  #  mean/std/min/max tek seferde çıkar.

    lines: List[str] = []
    lines.append("## 2. Temel İstatistikler")
    lines.append("")
    lines.append("| Sütun | Mean | Std | Min | Max |")
    lines.append("|------|------|-----|-----|-----|")

    for col in desc.index:
        mean = float(desc.loc[col, "mean"])
        std = float(desc.loc[col, "std"])
        mn = float(desc.loc[col, "min"])
        mx = float(desc.loc[col, "max"])
        lines.append(f"| {col} | {mean:.2f} | {std:.2f} | {mn:.2f} | {mx:.2f} |")

    lines.append("")
    return "\n".join(lines).strip()



def _generate_quality_section(context: Any) -> str:
    """
    Veri kalitesi bölümünü oluştur.
    
    TODO: Implement this function
    """
    
    df = getattr(context, "dataframe", None)  # context içinden df'yi güvenli al
    if df is None:  # df yoksa rapor üretilemez
        return "## 3. Veri Kalitesi\n\nVeri bulunamadı.\n"

    step_results = getattr(context, "step_results", None)  # analiz adım sonuçları

    # step_results list/dict olabilir; tek tipe çeviriyoruz
    step_map: Dict[str, Any] = (
        step_results
        if isinstance(step_results, dict)
        else {d.get("step"): d.get("result", {}) for d in step_results if isinstance(d, dict) and d.get("step")}
        if isinstance(step_results, list)
        else {}
    )

    lines: List[str] = []
    lines.append("## 3. Veri Kalitesi")  # bölüm başlığı
    lines.append("")

    # --- Eksik veri ---
    miss = step_map.get("check_missing", {}) or {}  # eksik veri step sonucu
    if isinstance(miss, dict) and miss:
        total_missing = int(miss.get("total_missing", 0) or 0)  # toplam eksik hücre
        miss_pct = float(miss.get("missing_percentage", 0) or 0.0)  # eksik %
    else:
        total_missing = int(df.isna().sum().sum())  # toplam eksik hücre
        total_cells = int(df.shape[0] * df.shape[1])  # toplam hücre
        miss_pct = (total_missing / total_cells * 100) if total_cells else 0.0  # eksik %

    lines.append(f"- Toplam eksik değer: **{total_missing}**")  # özet satır
    lines.append(f"- Eksik veri oranı: **%{miss_pct:.2f}**")  # yüzde format
    lines.append("")

    # Sütun bazında eksik veri 
    by_col = miss.get("by_column", {}) if isinstance(miss, dict) else {}  # sütun kırılımı
    if isinstance(by_col, dict) and by_col:
        items = sorted(
            by_col.items(),
            key=lambda x: float((x[1] or {}).get("percentage", 0) or 0),
            reverse=True,
        )  # eksik %'ye göre sırala

        lines.append("**Sütun Bazında Eksikler (ilk 5):**")  # kısa liste
        for col, info in items[:5]:
            cnt = int((info or {}).get("count", 0) or 0)  # eksik adet
            pct = float((info or {}).get("percentage", 0) or 0.0)  # eksik %
            lines.append(f"- `{col}`: {cnt} adet (**%{pct:.2f}**)")
        lines.append("")

    # --- Outlier ---
    outl = step_map.get("detect_outliers", {}) or {}  # outlier step sonucu
    if isinstance(outl, dict) and outl:
        total_outliers = int(outl.get("total_outliers", 0) or 0)  # toplam outlier
        lines.append(f"- Toplam outlier: **{total_outliers}**")

        warns = outl.get("warnings", []) or []  # uyarılar
        if isinstance(warns, list) and warns:
            lines.append("**Outlier Uyarıları:**")
            for w in warns[:5]:
                lines.append(f"- {w}")
    else:
        lines.append("- Outlier analizi sonucu bulunamadı.")  # step yoksa bilgi

    lines.append("")
    return "\n".join(lines).strip()  # markdown metni
    



def _generate_correlation_section(context: Any) -> str:
    """
    Korelasyon bölümünü oluştur.
    
    TODO: Implement this function
    """
    
    step_results = getattr(context, "step_results", None)  # adım sonuçları

    # step_results list/dict olabilir; tek tipe çeviriyoruz
    step_map: Dict[str, Any] = (
        step_results
        if isinstance(step_results, dict)
        else {d.get("step"): d.get("result", {}) for d in step_results if isinstance(d, dict) and d.get("step")}
        if isinstance(step_results, list)
        else {}
    )

    corr_res = step_map.get("find_correlations", {}) or {}  # korelasyon sonucu
    strong = corr_res.get("strong_correlations", []) if isinstance(corr_res, dict) else []  # güçlü korelasyonlar

    lines: List[str] = []
    lines.append("## 4. Korelasyonlar")  # bölüm başlığı
    lines.append("")

    if not (isinstance(strong, list) and strong):
        lines.append("- Güçlü korelasyon bulunamadı.")  # bilgi satırı
        lines.append("")
        return "\n".join(lines).strip()

    
    lines.append("| Değişken 1 | Değişken 2 | Korelasyon | Yorum |")  # tablo başlıkları
    lines.append("|-----------|-----------:|----------:|-------|")

    for item in strong[:10]:  # ilk 10 korelasyon
        if not isinstance(item, dict):
            continue
        c1 = item.get("col1")  # 1. değişken
        c2 = item.get("col2")  # 2. değişken
        val = item.get("correlation")  # korelasyon değeri
        strength = item.get("strength", "")  # yorum/metin
        if c1 and c2 and val is not None:
            lines.append(f"| {c1} | {c2} | {float(val):.3f} | {strength} |")

    lines.append("")
    return "\n".join(lines).strip()  # markdown metni




def _generate_conclusion_section(context: Any) -> str:
    """
    Sonuç ve öneriler bölümünü oluştur.
    
    TODO: Implement this function
    """
   
    step_results = getattr(context, "step_results", None)  # adım sonuçları

    # list/dict farkını tek tipe indiriyoruz
    step_map: Dict[str, Any] = (
        step_results
        if isinstance(step_results, dict)
        else {d.get("step"): d.get("result", {}) for d in step_results if isinstance(d, dict) and d.get("step")}
        if isinstance(step_results, list)
        else {}
    )

    miss = step_map.get("check_missing", {}) or {}  # eksik veri özeti
    outl = step_map.get("detect_outliers", {}) or {}  # outlier özeti
    corr = step_map.get("find_correlations", {}) or {}  # korelasyon özeti

    miss_pct = float(miss.get("missing_percentage", 0) or 0.0) if isinstance(miss, dict) else 0.0  # eksik %
    total_outl = int(outl.get("total_outliers", 0) or 0) if isinstance(outl, dict) else 0  # outlier sayısı
    strong = corr.get("strong_correlations", []) if isinstance(corr, dict) else []  # güçlü korelasyonlar
    strong_count = len(strong) if isinstance(strong, list) else 0  # corr sayısı

    insights = getattr(context, "insights", []) or []  # önemli bulgular

    lines: List[str] = []
    lines.append("## 5. Sonuç ve Öneriler")  # bölüm başlığı
    lines.append("")

    # kısa özet
    lines.append("**Kısa Özet:**")
    lines.append(f"- Eksik veri oranı: **%{miss_pct:.2f}**")
    lines.append(f"- Toplam outlier: **{total_outl}**")
    lines.append(f"- Güçlü korelasyon sayısı: **{strong_count}**")
    lines.append("")

    
    lines.append("**Öneriler / Bulgular:**")  # öneri/bulgu listesi
    if isinstance(insights, list) and insights:
        for x in insights[:8]:  # ilk 8 madde
            lines.append(f"- {x}")
    else:
        lines.append("- Ek bulgu/öneri bulunamadı.")

    lines.append("")
    return "\n".join(lines).strip()  # markdown metni





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
