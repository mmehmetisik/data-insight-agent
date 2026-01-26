# Agent Core (Planner & Executor)

## Genel Bakış

Agent Core modülü, Data Insight Agent'ın karar verme ve yürütme mantığını içerir. İki ana bileşenden oluşur:

- **Planner:** Veri setini analiz ederek LLM ile dinamik plan oluşturur
- **Executor:** Oluşturulan planı adım adım yürütür ve sonuçları yorumlar

Bu modül **Planning + Execution Pattern** kullanır: Agent önce düşünür (plan), sonra yürütür (execute). Bu yaklaşım sayesinde her veri setine özel, dinamik analiz stratejileri oluşturulur.

---

## Dosyalar

- `agent/planner.py` - Plan oluşturma ve LLM entegrasyonu
- `agent/executor.py` - Plan yürütme ve tool orchestration

---

## Planning + Execution Pattern

### Neden Bu Pattern?

**Geleneksel Yaklaşım:** Her veri seti için sabit analiz adımları  
**Bizim Yaklaşım:** LLM veriyi inceleyip duruma özel plan oluşturur

**Örnek:**
- 20K satırlık temiz veri → Korelasyon + outlier analizi öncelikli
- 500 satır, %40 eksik → Önce eksik veri analizi

---

## Planner Sınıfı

### Amaç
Veri seti hakkında bilgi alır (shape, columns, dtypes, missing) ve LLM ile analiz planı oluşturur.

### Ana Metodlar

#### `__init__()`
Groq client ve model ayarlarını başlatır.

```python
planner = Planner()
# Groq client: llama-3.3-70b-versatile
# System prompt yüklendi
```

---

#### `create_plan(data_info)`

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| data_info | dict | shape, columns, dtypes, missing içeren dict |

**Dönüş:**

| Alan | Tip | Açıklama |
|------|-----|----------|
| plan | List[Dict] | Her adım: step_number, action, description, tool |

**Örnek Kullanım:**
```python
data_info = {
    "shape": (891, 12),
    "columns": ["Age", "Fare", "Survived"],
    "dtypes": {"Age": "float64"},
    "missing": {"Age": 177}
}

plan = planner.create_plan(data_info)
# [{"step_number": 1, "action": "load_and_inspect", ...}]
```

---

#### `_format_data_info(data_info)`

Veri bilgisini LLM'in anlayabileceği formata çevirir.

**Input:** Python dict  
**Output:** Formatlanmış string

```
Boyut: 891 satır, 12 sütun
Sütunlar:
- Age: float64 (177 eksik)
- Fare: float64
```

---

#### `_call_llm(prompt)`

Groq API üzerinden LLM'i çağırır.

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| prompt | str | Kullanıcı promptu |

**Dönüş:** LLM cevabı (string)

API hataları yakalanır ve anlamlı hata mesajı döner.

---

#### `_parse_plan(llm_response)`

LLM'den gelen JSON'ı Python listesine çevirir.

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| llm_response | str | LLM'den gelen JSON (veya JSON + metin) |

**Dönüş:**

| Alan | Tip | Açıklama |
|------|-----|----------|
| plan | List[Dict] | Validate edilmiş plan adımları |

**Özellikler:**
- Code block marker'ları temizler (```json)
- Açıklama metinlerini ayıklar
- Geçersiz adımları filtreler

**Örnek Input:**
```
Analiz planı:
```json
{"plan": [{"step_number": 1, "action": "load_and_inspect", ...}]}
```
```

**Output:**
```python
[{"step_number": 1, "action": "load_and_inspect", ...}]
```

---

## Executor Sınıfı

### Amaç
Planner'ın oluşturduğu planı alır, her adımı sırayla yürütür. Her adımda uygun tool'u çağırır, sonucu context'e kaydeder ve LLM ile yorumlar.

### Ana Metodlar

#### `__init__()`

Groq client ve tool registry'sini başlatır.

**Tool Registry:**
```python
{
    "load_and_inspect": load_and_inspect,
    "compute_statistics": compute_statistics,
    "check_missing": check_missing,
    "find_correlations": find_correlations,
    "detect_outliers": detect_outliers,
    "generate_summary": generate_summary
}
```

Bu yapı action adına göre fonksiyon seçimi yapar (Strategy Pattern benzeri).

---

#### `execute_plan(plan, context)`

Planı adım adım yürütür ve her adımın sonucunu **yield** eder.

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| plan | List[Dict] | Planner'dan gelen plan |
| context | ExecutionContext | Agent'ın hafızası |

**Yields:**

| Alan | Tip | Açıklama |
|------|-----|----------|
| step_number | int | Adım numarası |
| total_steps | int | Toplam adım sayısı |
| action | str | Yapılan işlem |
| description | str | Türkçe açıklama |
| result | dict | Tool sonucu |
| interpretation | str | LLM yorumu |
| status | str | "success" veya "error" |

**Örnek Kullanım:**
```python
for step_result in executor.execute_plan(plan, context):
    print(f"Adım {step_result['step_number']}: {step_result['status']}")
    print(f"Yorum: {step_result['interpretation']}")
```

**Neden Generator?** Streamlit'te real-time progress göstermek için. Her adım tamamlanınca anında UI'a yansır.

---

#### `_execute_step(step, context)`

Tek bir plan adımını yürütür.

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| step | Dict | Plan adımı |
| context | ExecutionContext | Agent hafızası |

**Dönüş:**

| Alan | Tip | Açıklama |
|------|-----|----------|
| result | Dict | Tool sonucu veya hata bilgisi |

**Akış:**
1. Tool registry'den action'a uygun fonksiyonu bul
2. Fonksiyonu çağır
3. Sonucu döndür
4. Hata varsa error dict döndür

---

#### `_interpret_result(step, result, context)`

Adım sonucunu LLM ile Türkçe yorumlar.

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| step | Dict | Yapılan adım |
| result | Dict | Adım sonucu |
| context | ExecutionContext | Geçmiş adımlar |

**Dönüş:** Türkçe yorum (string)

**Prompt Yapısı:**
```
Adım: Eksik değerleri analiz et
İşlem: check_missing

Sonuç:
{'missing_count': 177, 'percentage': 19.8}

Bu sonucu 2-3 cümle ile Türkçe yorumla.
```

**Örnek Çıktı:**
```
"Age sütununda 177 eksik değer bulundu (%19.8). 
Bu oran analiz sonuçlarını etkileyebilir."
```

---

#### `_call_llm(prompt)`

Groq API'yi çağırır (Planner'daki ile aynı mantık).

**Parametreler:**

| Parametre | Tip | Açıklama |
|-----------|-----|----------|
| prompt | str | Kullanıcı promptu |

**Dönüş:** LLM cevabı (string)

---

## Tool Registry Yapısı

Tool registry, action adını fonksiyona eşleyen bir dictionary:

```python
self.tool_registry = {
    "load_and_inspect": load_and_inspect,
    "compute_statistics": compute_statistics,
    ...
}
```

**Kullanım:**
```python
action = "load_and_inspect"
tool_func = self.tool_registry.get(action)
result = tool_func(context)
```

**Avantajlar:**
- Yeni tool eklemek kolay
- If-elif zincirine gerek yok
- Dinamik fonksiyon çağırma

---

## Generator Pattern (yield) Kullanımı

### Neden Generator?

**Geleneksel:**
```python
def execute_plan(plan):
    results = []
    for step in plan:
        results.append(execute_step(step))
    return results  # Tüm adımlar bitince döner
```

**Generator:**
```python
def execute_plan(plan):
    for step in plan:
        yield execute_step(step)  # Her adım bitince döner
```

### Avantajlar

1. **Real-Time Progress:** Her adım UI'da anında görünür
2. **Memory Efficient:** Tüm sonuçları bellekte tutmaya gerek yok
3. **Early Termination:** Kritik hatada kalan adımlar atlanabilir

### Streamlit'te Kullanım

```python
# app.py
for step_result in executor.execute_plan(plan, context):
    with st.expander(f"Adım {step_result['step_number']}"):
        st.write(step_result['interpretation'])
```

---

## LLM Entegrasyonu

### Planner'da LLM

**Girdi:** Veri bilgisi (shape, columns, missing)  
**Çıktı:** JSON formatında plan

**System Prompt İçeriği:**
- Kullanılabilir tool'lar
- JSON format kuralları
- Türkçe çıktı gereksinimi
- Maksimum 6 adım limiti

---

### Executor'da LLM

**Girdi:** Adım sonucu (raw data)  
**Çıktı:** İnsan dostu Türkçe açıklama

**System Prompt İçeriği:**
- Kısa yorumlar (2-3 cümle)
- Önemli bulguları vurgula
- Anlaşılır dil

---

## Karşılaşılan Zorluklar

### 1. Groq Model Değişikliği

**Sorun:** `llama-3.1-70b-versatile` modeli kullanımdan kaldırıldı  
**Hata:** `Error code: 400 - model has been decommissioned`  
**Çözüm:** `config.py`'da model `llama-3.3-70b-versatile` olarak güncellendi  
**Ders:** API sağlayıcıları modelleri düzenli güncelliyor, merkezi konfigürasyon önemli

---

### 2. JSON Parsing - LLM Ek Metin Sorunu

**Sorun:** LLM JSON'dan önce açıklama ekliyordu  
**Örnek:** `"Analiz planı:\n```json..."`  
**Hata:** `JSONDecodeError: Expecting value`  
**Çözüm:**
- `_parse_plan()` metodunda substring extraction
- Code block marker'ları temizleme (```json)
- Prompt'a ek kural: "SADECE JSON döndür"

**Ders:** LLM'ler format kurallarına her zaman uymaz, defensive parsing gerekli

---

### 3. Module Import Path

**Sorun:** `ModuleNotFoundError: No module named 'config'`  
**Neden:** `planner.py` `agent/` klasöründe, `config.py` üst klasörde  
**Çözüm:**
```python
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```
**Ders:** Modüler projelerde path yönetimi kritik

---

### 4. Groq Package Version

**Sorun:** `TypeError: Client.__init__() got unexpected keyword argument`  
**Neden:** groq==0.4.2 → groq==1.0.0 arasında breaking change  
**Çözüm:** `pip install --upgrade groq`  
**Ders:** Major version değişimleri (0.x → 1.x) API'yi değiştirebilir

---

## Edinilen Deneyimler

### Defensive Parsing
LLM çıktısı her zaman beklendiği formatta gelmez:
- Code block marker'ları temizle
- Ek metinleri ayıkla
- Try-except ile hata yakala
- Geçersiz adımları filtrele

### Error Handling
Her seviyede error handling gerekli:
- API seviyesi (Groq bağlantısı)
- Parse seviyesi (JSON parsing)
- Execution seviyesi (Tool çağrısı)
- Application seviyesi (Streamlit UI)

### Tool Registry Pattern
Dictionary-based mapping basit ama güçlü:
- Yeni tool eklemek kolay
- If-elif karmaşası yok
- Test edilebilir

### Generator Pattern
Real-time feedback için vazgeçilmez:
- Kullanıcı deneyimi çok daha iyi
- Progress tracking doğal olarak gelir
- Memory verimli

### LLM Prompt Engineering
Prompt kalitesi output kalitesini direkt etkiler:
- Kuralları net belirt
- Format örnekleri göster
- Kısıtlamaları açıkla
- Çıktı dilini vurgula

### Git Workflow
Modüler geliştirmede:
- Her kişi kendi branch'inde çalışır
- Bağımlılıklar için geçici çözümler kullanılır
- PR'lar küçük ve odaklı olmalı
- Code review sürecinden çok şey öğrenilir

---

## Geliştirme Fırsatları

### Plan Revizyonu (Adaptive Planning)
**Mevcut:** Plan bir kere oluşturulur  
**Öneri:** Execution sırasında beklenmedik bulgularda planı revize et

Örnek: Adım 2'de %40 eksik veri bulunursa, plan otomatik güncellenir

### Caching
**Mevcut:** Her adımda LLM çağrısı  
**Öneri:** Benzer sonuçlar için cache kullan

### Error Recovery
**Mevcut:** Hata işaretlenir, devam edilir  
**Öneri:** Rate limit gibi geçici hatalar için otomatik retry

### Tool Parametreleri
**Mevcut:** Tool'lar sadece context alıyor  
**Öneri:** Planner, tool'lara parametre gönderebilir

```python
{
    "action": "find_correlations",
    "parameters": {"threshold": 0.7, "method": "pearson"}
}
```

### Multi-LLM Desteği
**Mevcut:** Sadece Groq API  
**Öneri:** Farklı LLM'ler için adapter pattern

---

## Örnek Akış

```
1. Kullanıcı CSV yükler
   ↓
2. Planner.create_plan(data_info)
   → LLM'e veri bilgisi gönderilir
   → Plan JSON olarak döner
   → Parse edilir
   ↓
3. Executor.execute_plan(plan, context)
   → Adım 1: load_and_inspect()
     → Sonuç context'e kaydedilir
     → LLM yorumlar: "891 satır, 12 sütun..."
     → yield {"status": "success", ...}
   ↓
   → Adım 2: compute_statistics()
     → LLM yorumlar: "Ortalama yaş 29.7..."
     → yield {"status": "success", ...}
   ↓
   → Son Adım: generate_summary()
     → Markdown rapor oluşturulur
   ↓
4. Streamlit her yield'de UI'ı günceller
   ↓
5. Kullanıcı raporu indirir
```

---

## Sonuç

Agent Core modülü, Planning + Execution Pattern'ini başarıyla uygular. LLM entegrasyonu, defensive parsing, generator pattern ve tool orchestration kombinasyonu esnek ve güçlü bir sistem oluşturur.

En önemli öğrenim: LLM'ler güçlü ama öngörülemez. Defensive programming ve kapsamlı error handling ile bu öngörülemezlik yönetilebilir.
