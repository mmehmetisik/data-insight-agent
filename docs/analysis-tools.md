# Analysis & Reporter Tools

Bu dokümantasyon, proje içinde veri seti üzerinde **eksik değer analizi**, **korelasyon analizi**, **outlier tespiti** ve bu çıktılardan **Markdown rapor üretimi** yapan araçları tanımlar. Modüller, `ExecutionContext` benzeri bir context nesnesi üzerinden `pandas.DataFrame` alır ve çıktıları standart bir sözlük (dict) yapısı ile döndürür. Amaç, agent akışı içinde otomatik ve tekrar kullanılabilir analiz adımları üretmektir.

## Genel Bakış

Bu dokümantasyon, projede **analiz adımlarını** üreten `analysis.py` ve bu adımların çıktılarından **Markdown rapor** oluşturan `reporter.py` araçlarını kapsar.

- **`tools/analysis.py`**: Veri setinde eksik değer analizi, korelasyon analizi ve IQR tabanlı outlier tespiti yapar.
- **`tools/reporter.py`**: Agent akışında biriken analiz çıktılarından Markdown formatında özet rapor üretir.

Tüm fonksiyonlar standart bir sözlük (dict) çıktısı döndürür:

- Başarı durumu `success` alanı ile işaretlenir.
- Hata durumlarında mümkünse açıklayıcı `error` alanı döndürülür.
- Eşikler/çarpanlar `config.py` içindeki sabitlerden alınır.

## Dosyalar

- `tools/analysis.py` — Eksik veri, korelasyon ve outlier analiz fonksiyonları.
- `tools/reporter.py` — Analiz sonuçlarından Markdown rapor oluşturma ve rapor alt bölüm üreticileri.
- `config.py` — Eşik/çarpan gibi konfigürasyon sabitleri:
  - `CORRELATION_THRESHOLD`
  - `MISSING_DATA_WARNING_THRESHOLD`
  - `OUTLIER_IQR_MULTIPLIER`

## Ana Fonksiyonlar

Bu fonksiyonlar, agent tarafından sağlanan bir **context** nesnesi üzerinden çalışır. Minimum gereksinim: `context.dataframe` içinde bir `pandas.DataFrame` bulunmasıdır. Rapor üretiminde (varsa) `context.step_results` ve `context.insights` alanları kullanılır.

### `check_missing(context)`

**Amaç:**  
DataFrame içindeki eksik değerleri analiz eder. Genel eksik oranını (`missing_percentage`) hesaplar, sütun bazında eksik adet/yüzde çıkarır ve konfigürde tanımlanan eşik değerine göre uyarılar üretir.

**Parametreler:**

| Parametre | Tip | Açıklama                                                      |
| --------- | --- | ------------------------------------------------------------- |
| context   | Any | `context.dataframe` alanında `pandas.DataFrame` taşıyan nesne |

**Dönüş Değeri:**

| Alan               | Tip       | Açıklama                              |
| ------------------ | --------- | ------------------------------------- |
| success            | bool      | İşlem başarılı mı                     |
| total_missing      | int       | Toplam eksik hücre sayısı             |
| total_cells        | int       | Toplam hücre sayısı (`satır * sütun`) |
| missing_percentage | float     | Genel eksik veri yüzdesi (1 ondalık)  |
| by_column          | dict      | Sütun bazında `count` ve `percentage` |
| warnings           | list[str] | Eşik aşımı varsa uyarı metinleri      |
| error              | str       | (opsiyonel) Hata mesajı               |

**Notlar / Mantık:**

- Eşik değeri `MISSING_DATA_WARNING_THRESHOLD` üzerinden okunur.
- Eşik `0 < thr <= 1` aralığındaysa **oran** kabul edilip yüzdeye çevrilir (`thr * 100`).
- Sütun bazında eksik oranı `%50` ve üzerindeyse aksiyon mesajı “analizden çıkarılabilir”, altında ise “doldurmak gerekebilir” olarak üretilir.
- Boş DataFrame durumunda güvenli şekilde boş sonuç döndürür.

**Örnek Kullanım:**

```python
from tools.analysis import check_missing

result = check_missing(context)
if result["success"]:
    print("Genel eksik %:", result["missing_percentage"])
    print("Uyarılar:", result["warnings"])
else:
    print("Hata:", result.get("error"))
```

> ### `find_correlations(context)`
>
> **Amaç:**  
> Yalnızca sayısal sütunlar üzerinde korelasyon matrisi hesaplar ve `CORRELATION_THRESHOLD` eşiğini aşan güçlü korelasyon çiftlerini listeler.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                                      |
> | --------- | ----- | ------------------------------------------------------------- |
> | `context` | `Any` | `context.dataframe` alanında `pandas.DataFrame` taşıyan nesne |
>
> **Dönüş Değeri:**
>
> | Alan                  | Tip          | Açıklama                                     |
> | --------------------- | ------------ | -------------------------------------------- |
> | `success`             | `bool`       | İşlem başarılı mı                            |
> | `correlation_matrix`  | `dict[dict]` | Korelasyon matrisi (3 ondalık, dict-of-dict) |
> | `strong_correlations` | `list[dict]` | Güçlü korelasyon listesi                     |
> | `warnings`            | `list[str]`  | Bilgilendirme/uyarı mesajları                |
> | `error`               | `str`        | (opsiyonel) Hata mesajı                      |
>
> **`strong_correlations` öğe formatı:**
>
> - `col1`: 1. sütun adı
> - `col2`: 2. sütun adı
> - `correlation`: korelasyon değeri (3 ondalık)
> - `strength`: metinsel etiket (`strong/moderate positive/negative`)
>
> **Notlar / Mantık:**
>
> - En az 2 sayısal sütun yoksa boş sonuç + uyarı döndürür: `Korelasyon için yeterli sayısal sütun yok.`
> - Matris `numeric_df.corr()` ile üretilir ve `to_dict()` ile sözlüğe çevrilir.
> - Güç etiketleme, eşik (`CORRELATION_THRESHOLD`) ve `0.7` sınırına göre yapılır:
>   - `corr >= 0.7`: `strong positive`
>   - `thr <= corr < 0.7`: `moderate positive`
>   - `corr <= -0.7`: `strong negative`
>   - `-0.7 < corr <= -thr`: `moderate negative`
>
> **Örnek Kullanım:**
>
> ```python
> from tools.analysis import find_correlations
>
> result = find_correlations(context)
> if result["success"]:
>     for item in result["strong_correlations"][:10]:
>         print(item["col1"], item["col2"], item["correlation"], item["strength"])
> else:
>     print("Hata:", result.get("error"))
> ```

---

> ### `detect_outliers(context)`
>
> **Amaç:**  
> Sayısal sütunlarda IQR yöntemiyle aykırı değerleri tespit eder. Her sütun için alt/üst sınırları, outlier sayısını, outlier yüzdesini ve örnek outlier değerlerini raporlar.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                                      |
> | --------- | ----- | ------------------------------------------------------------- |
> | `context` | `Any` | `context.dataframe` alanında `pandas.DataFrame` taşıyan nesne |
>
> **Dönüş Değeri:**
>
> | Alan             | Tip         | Açıklama                                    |
> | ---------------- | ----------- | ------------------------------------------- |
> | `success`        | `bool`      | İşlem başarılı mı                           |
> | `by_column`      | `dict`      | Sütun bazında outlier bilgisi               |
> | `total_outliers` | `int`       | Toplam outlier sayısı                       |
> | `outlier_rows`   | `list`      | Outlier içeren satır index’leri (benzersiz) |
> | `warnings`       | `list[str]` | Uyarılar (örn. %10+ outlier)                |
> | `error`          | `str`       | (opsiyonel) Hata mesajı                     |
>
> **IQR Yöntemi:**
>
> - `Q1 = 0.25 quantile`, `Q3 = 0.75 quantile`
> - `IQR = Q3 - Q1`
> - `lower = Q1 - OUTLIER_IQR_MULTIPLIER * IQR`
> - `upper = Q3 + OUTLIER_IQR_MULTIPLIER * IQR`
> - Aralık dışı değerler outlier kabul edilir.
>
> **Notlar / Mantık:**
>
> - Sayısal sütun yoksa uyarı döndürür: `Outlier analizi için sayısal sütun bulunamadı.`
> - `outlier_values` çok büyümesin diye en fazla **ilk 20** değer tutulur.
> - Outlier yüzdesi `%10` ve üzerindeyse `warnings` listesine mesaj eklenir.
>
> **Örnek Kullanım:**
>
> ```python
> from tools.analysis import detect_outliers
>
> result = detect_outliers(context)
> if result["success"]:
>     print("Toplam outlier:", result["total_outliers"])
>     print("Uyarılar:", result["warnings"])
>     print("Outlier satırları (ilk 10):", result["outlier_rows"][:10])
> else:
>     print("Hata:", result.get("error"))
> ```

---

> ### `generate_summary(context)`
>
> **Amaç:**  
> `context` üzerinde biriken analiz sonuçlarından (özellikle `context.step_results` ve `context.insights`) **Markdown formatında** özet rapor üretir. Rapor; genel bakış, istatistikler, veri kalitesi, korelasyonlar ve sonuç/öneriler bölümlerini içerir.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                                                                |
> | --------- | ----- | --------------------------------------------------------------------------------------- |
> | `context` | `Any` | `context.dataframe` (zorunlu), `context.step_results` ve `context.insights` (opsiyonel) |
>
> **Dönüş Değeri:**
>
> | Alan              | Tip           | Açıklama                      |
> | ----------------- | ------------- | ----------------------------- |
> | `success`         | `bool`        | İşlem başarılı mı             |
> | `report_markdown` | `str`         | Markdown rapor metni          |
> | `report_html`     | `str \| None` | Opsiyonel (bu sürümde `None`) |
> | `key_findings`    | `list[str]`   | Öne çıkan bulgular (maks. 10) |
> | `error`           | `str`         | (opsiyonel) Hata mesajı       |
>
> **Notlar / Mantık:**
>
> - `report_markdown` içeriği `_create_markdown_report(context)` ile üretilir.
> - `key_findings` listesi:
>   - İlk madde: `Veri seti X satır ve Y sütun içermektedir`
>   - Sonra `context.insights` içinden (varsa) ilk 5 madde eklenir.
>   - Tekrarlar temizlenir, maksimum 10 madde tutulur.
>
> **Örnek Kullanım:**
>
> ```python
> from tools.reporter import generate_summary
>
> result = generate_summary(context)
> if result["success"]:
>     print(result["report_markdown"][:800])
>     print("Key findings:", result["key_findings"])
> else:
>     print("Hata:", result.get("error"))
> ```

## Diğer Fonksiyonlar ve Yardımcılar

> Not: Bunlar “internal/helper” fonksiyonlardır. Genellikle doğrudan çağrılmaz; `generate_summary()` içinden kullanılır.

---

> ### `_create_markdown_report(context)`
>
> **Amaç:**  
> Raporun ana gövdesini üretir; bölümleri alt fonksiyonlardan alır ve tek bir Markdown metninde birleştirir.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                                  |
> | --------- | ----- | --------------------------------------------------------- |
> | `context` | `Any` | `context.dataframe` içeren ExecutionContext benzeri nesne |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                        |
> | -------- | ----- | ------------------------------- |
> | (return) | `str` | Markdown formatında rapor metni |
>
> **Kullandığı Alt Bölümler:**
>
> - `_generate_overview_section(context)`
> - `_generate_statistics_section(context)`
> - `_generate_quality_section(context)`
> - `_generate_correlation_section(context)`
> - `_generate_conclusion_section(context)`

---

> ### `_generate_overview_section(context)`
>
> **Amaç:**  
> “Genel Bakış” bölümünü üretir. Veri setinin boyutunu, sayısal/kategorik sütun adetlerini ve ilk 10 sütunun veri tiplerini listeler.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                           |
> | --------- | ----- | ---------------------------------- |
> | `context` | `Any` | `context.dataframe` alanı beklenir |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                            |
> | -------- | ----- | ----------------------------------- |
> | (return) | `str` | Markdown metni (Genel Bakış bölümü) |
>
> **Notlar / Mantık:**
>
> - İlk 10 sütun dtype bilgisi rapor şişmesin diye limitlidir.
> - `context.dataframe` yoksa “Veri bulunamadı.” döndürür.

---

> ### `_generate_statistics_section(context)`
>
> **Amaç:**  
> Sayısal sütunların temel istatistiklerini (mean, std, min, max) tablo formatında üretir.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                           |
> | --------- | ----- | ---------------------------------- |
> | `context` | `Any` | `context.dataframe` alanı beklenir |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                              |
> | -------- | ----- | ------------------------------------- |
> | (return) | `str` | Markdown metni (İstatistikler bölümü) |
>
> **Notlar / Mantık:**
>
> - Sadece sayısal sütunlar (`include="number"`) seçilir.
> - `describe().T` ile sütun bazlı tablo üretilir.
> - Sayısal sütun yoksa bilgi mesajı döndürür.

---

> ### `_generate_quality_section(context)`
>
> **Amaç:**  
> “Veri Kalitesi” bölümünü üretir. Eksik değer özetini ve outlier özetini raporlar. Analiz adımları daha önce çalıştırıldıysa `context.step_results` içinden `check_missing` ve `detect_outliers` sonuçlarını kullanır.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                               |
> | --------- | ----- | ------------------------------------------------------ |
> | `context` | `Any` | `context.dataframe` ve tercihen `context.step_results` |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                              |
> | -------- | ----- | ------------------------------------- |
> | (return) | `str` | Markdown metni (Veri Kalitesi bölümü) |
>
> **Notlar / Mantık:**
>
> - `step_results` hem `dict` hem `list[dict]` olabilir; önce `step_map`’e normalize edilir.
> - Missing sonucu yoksa DataFrame’den fallback hesap yapılır (`df.isna().sum().sum()`).
> - Sütun bazında eksik veri varsa en yüksek eksik yüzdeli ilk 5 sütun listelenir.
> - Outlier sonucu yoksa “Outlier analizi sonucu bulunamadı.” yazar.

---

> ### `_generate_correlation_section(context)`
>
> **Amaç:**  
> “Korelasyonlar” bölümünü üretir. `context.step_results` içinden `find_correlations` sonucunu alır ve `strong_correlations` listesini tabloya döker.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                 |
> | --------- | ----- | ---------------------------------------- |
> | `context` | `Any` | Tercihen `context.step_results` içermeli |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                              |
> | -------- | ----- | ------------------------------------- |
> | (return) | `str` | Markdown metni (Korelasyonlar bölümü) |
>
> **Notlar / Mantık:**
>
> - Güçlü korelasyon yoksa “Güçlü korelasyon bulunamadı.” döndürür.
> - Tabloya maksimum ilk 10 korelasyon yazılır.

---

> ### `_generate_conclusion_section(context)`
>
> **Amaç:**  
> “Sonuç ve Öneriler” bölümünü üretir. Eksik veri oranı, toplam outlier ve güçlü korelasyon sayısı gibi metrikleri özetler; ayrıca `context.insights` varsa ilk maddeleri öneriler/bulgular altında listeler.
>
> **Parametreler:**
>
> | Parametre | Tip   | Açıklama                                               |
> | --------- | ----- | ------------------------------------------------------ |
> | `context` | `Any` | `context.step_results` ve opsiyonel `context.insights` |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                                  |
> | -------- | ----- | ----------------------------------------- |
> | (return) | `str` | Markdown metni (Sonuç ve Öneriler bölümü) |
>
> **Notlar / Mantık:**
>
> - `step_results` normalize edilip şu adımlar okunur: `check_missing`, `detect_outliers`, `find_correlations`.
> - `context.insights` boşsa “Ek bulgu/öneri bulunamadı.” döndürür.
> - Insight listesi varsa en fazla ilk 8 madde yazılır.

> ### `_get_correlation_strength(corr)`
>
> **Amaç:**  
> Korelasyon değerinin mutlak büyüklüğüne göre (strong/moderate/weak/negligible) ve işaretine göre (positive/negative) metinsel bir etiket üretir.
>
> **Parametreler:**
>
> | Parametre | Tip     | Açıklama                           |
> | --------- | ------- | ---------------------------------- |
> | `corr`    | `float` | Korelasyon değeri (-1 ile 1 arası) |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                |
> | -------- | ----- | ----------------------- |
> | (return) | `str` | Korelasyon gücü etiketi |
>
> **Etiket Kuralları:**
>
> - `|corr| >= 0.7`: `strong positive/negative`
> - `|corr| >= 0.5`: `moderate positive/negative`
> - `|corr| >= 0.3`: `weak positive/negative`
> - `|corr| < 0.3`: `negligible`
>
> **Not:**  
> Bu helper mevcut kodda tanımlı olsa da `find_correlations()` içinde ayrı bir etiketleme mantığı da var. İleride tekrarları azaltmak için refactor edilebilir.
>
> **Örnek Kullanım:**
>
> ```python
> from tools.analysis import _get_correlation_strength
> print(_get_correlation_strength(0.85))   # strong positive
> print(_get_correlation_strength(-0.4))   # weak negative
> print(_get_correlation_strength(0.1))    # negligible
> ```

> ### `format_number(value, decimals=2)`
>
> **Amaç:**  
> Sayısal değerleri okunabilir formatta yazdırır (binlik ayraç + istenen ondalık).
>
> **Parametreler:**
>
> | Parametre  | Tip                   | Açıklama                               |
> | ---------- | --------------------- | -------------------------------------- |
> | `value`    | `float \| int \| Any` | Formatlanacak sayı                     |
> | `decimals` | `int`                 | Ondalık basamak sayısı (varsayılan: 2) |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                |
> | -------- | ----- | ----------------------- |
> | (return) | `str` | Formatlanmış sayı metni |
>
> **Örnek Kullanım:**
>
> ```python
> from tools.reporter import format_number
> print(format_number(1234567.89))   # 1,234,567.89
> print(format_number(0.12345, 3))   # 0.123
> ```

---

> ### `format_percentage(value, decimals=1)`
>
> **Amaç:**  
> Yüzde değerlerini istenen ondalıkla formatlar (örn. `45.7%`).
>
> **Parametreler:**
>
> | Parametre  | Tip            | Açıklama                               |
> | ---------- | -------------- | -------------------------------------- |
> | `value`    | `float \| Any` | Yüzde değeri (0–100 arası beklenir)    |
> | `decimals` | `int`          | Ondalık basamak sayısı (varsayılan: 1) |
>
> **Dönüş Değeri:**
>
> | Alan     | Tip   | Açıklama                 |
> | -------- | ----- | ------------------------ |
> | (return) | `str` | Formatlanmış yüzde metni |
>
> **Örnek Kullanım:**
>
> ```python
> from tools.reporter import format_percentage
> print(format_percentage(45.678))    # 45.7%
> print(format_percentage(1.234, 2))  # 1.23%
> ```

---

## Akış Diyagramı

> ```mermaid
> flowchart LR
>   A[context.dataframe] --> B[check_missing]
>   A --> C[detect_outliers]
>   A --> D[find_correlations]
>   B --> E[context.step_results]
>   C --> E
>   D --> E
>   E --> F[generate_summary]
>   F --> G[report_markdown]
> ```

## Örnek Çıktılar

> ### `check_missing(context)` — örnek
>
> ```json
> {
>   "success": true,
>   "total_missing": 866,
>   "missing_percentage": 8.1,
>   "by_column": { "Age": { "count": 177, "percentage": 19.87 } },
>   "warnings": [
>     "Cabin sütununda %77.1 eksik veri var - bu sütun analizden çıkarılabilir"
>   ]
> }
> ```

> ### `find_correlations(context)` — örnek
>
> ```json
> {
>   "success": true,
>   "strong_correlations": [
>     {
>       "col1": "Fare",
>       "col2": "Pclass",
>       "correlation": -0.549,
>       "strength": "moderate negative"
>     }
>   ],
>   "warnings": []
> }
> ```

> ### `detect_outliers(context)` — örnek
>
> ```json
> {
>   "success": true,
>   "by_column": {
>     "Fare": {
>       "outlier_count": 116,
>       "outlier_percentage": 13.02,
>       "lower_bound": -26.7,
>       "upper_bound": 65.6
>     }
>   },
>   "total_outliers": 127,
>   "outlier_rows": [0, 1, 7],
>   "warnings": ["Fare sütununda %13 outlier var"]
> }
> ```

> ### `generate_summary(context)` — rapor başı örnek
>
> ```markdown
> # Veri Analiz Raporu
>
> ## **Oluşturma Tarihi:** 2026-01-26 12:00
>
> ## 1. Genel Bakış
>
> | Özellik      | Değer |
> | ------------ | ----- |
> | Satır Sayısı | 891   |
> | Sütun Sayısı | 12    |
> ```

## Öğrenilen Dersler

> - `context` tabanlı tasarım sayesinde her analiz fonksiyonu aynı nesneden (context) veriyi alıp sonuçları yine aynı yere

     yazabildiği için, adımlar ayrı ayrı parametre taşımadan peş peşe çalıştırılabiliyor; böylece analiz çıktıları tek bir yerde toplanıp
     rapora kolayca dönüştürülebiliyor.

> - `step_results` (list/dict) normalize etmek raporu dayanıklı hale getirdi.
> - Çıktı boyutunu sınırlamak (örn. ilk 5 sütun, ilk 20 outlier) okunabilirliği artırdı.
> - Konfigürasyon eşiklerini tek yerden yönetmek (config.py) bakım maliyetini düşürdü.

## İyileştirme Önerileri

> - `report_html` desteği eklenebilir. (Markdown → HTML) ve Streamlit daha zengin gösterilir.
> - Performans için, büyük veri setlerinde korelasyon hesaplaması zaman alacağından örnekleme / sütun limiti eklenebilir.
> - Outlier için aksiyon önerileri eklenebilir (winsorize, log dönüşümü, robust scaler).
>   - **Winsorize:** Uç değerleri tamamen silmek yerine, belirli alt/üst yüzdelik sınırlarına kırparak etkisini azaltır.
>   - **Log dönüşümü:** Sağa çarpık (çok büyük değerler içeren) dağılımlarda uç değerlerin etkisini yumuşatır.
>   - **Robust Scaler:** Ölçekleme yaparken ortalama-standart sapma yerine medyan ve IQR kullandığı için outlier'lardan daha az etkilenir.

> - > - Korelasyon metodu parametreleştirilebilir (Pearson / Spearman / Kendall).
>   - `find_correlations()` içinde korelasyon hesabında kullanılan yöntemi sabit tutmak yerine bir parametre ile seçilebilir yapmak.
>   - **Pearson:** Lineer ilişkiyi ölçer. Sayısal ve yaklaşık normal dağılımlı verilerde uygundur.
>   - **Spearman:** Sıralama (rank) üzerinden ölçer; doğrusal olmak zorunda olmayan ama **monoton** ilişkileri daha iyi yakalar.
>   - **Kendall:** Rank tabanlıdır; küçük örneklemlerde ve çok bağ (tie) olan verilerde daha sağlam olabilir.
