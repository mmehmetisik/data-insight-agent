# Memory & Prompts
## Genel Bakış

Bu modülün amacı, agent mimarisi içinde analiz sürecine ait execution context bilgisini merkezi olarak yönetmektir.
ExecutionContext; kullanılan veri setini, analiz adımlarını, ara sonuçları ve önemli bulguları tek bir yapı altında toplar.
Her adımın sonucu zaman bilgisiyle kaydedilerek sürecin izlenebilir olması sağlanır.
Toplanan bilgiler, LLM’e gönderilmek üzere bağlama uygun ve özet bir metin haline getirilir.
Prompt modülü ise planlama, yürütme ve yorumlama aşamalarında LLM ile tutarlı ve Türkçe etkileşim kurulmasını sağlar.


memory/context.py – Agent’ın analiz sürecine ait veri setini, adım sonuçlarını, planı ve önemli bulguları yöneterek LLM’e gönderilecek bağlamı oluşturan execution context yapısını içerir.

agent/prompts.py – Agent’ın planlama, yürütme ve yorumlama aşamalarında LLM ile etkileşimini yöneten Türkçe system prompt’ları ve mesaj şablonlarını tanımlar.

---


## Stateful vs Stateless Agent

Stateless agent’lar, her isteği birbirinden bağımsız olarak ele alır ve önceki adımlara ait herhangi bir durumu veya bağlamı hatırlamaz. Bu yaklaşım basit senaryolar için yeterli olsa da, çok adımlı analiz süreçlerinde tutarsız sonuçlara ve tekrar eden hesaplamalara yol açabilir.

Stateful agent’lar ise analiz süreci boyunca oluşan durumu merkezi bir yapı altında saklayarak, önceki adımlarda elde edilen sonuçları ve bulguları sonraki adımlarda kullanabilir. Bu sayede analiz akışı izlenebilir, kararlar daha tutarlı hale gelir ve LLM’in bağlamı kaybetmesi engellenir.

Bu projede stateful yaklaşım tercih edilmiştir. ExecutionContext sınıfı; veri seti bilgilerini, tamamlanan analiz adımlarını, ara sonuçları ve önemli bulguları saklayarak agent’ın “hafızası” gibi çalışır. Böylece LLM’e her seferinde yalnızca gerekli ve anlamlı bağlam iletilir.

Stateful yapı sayesinde analiz süreci kesintiye uğrasa bile, mevcut durum korunabilir ve süreç kontrollü şekilde devam ettirilebilir. Bu yaklaşım, özellikle karmaşık ve çok adımlı veri analizlerinde agent mimarisinin güvenilirliğini artırır.


---


## Dosyalar

* **memory/context.py** – Agent’ın analiz sürecine ait veri setini, adım sonuçlarını, planı ve önemli bulguları yöneterek LLM’e gönderilecek bağlamı oluşturan execution context yapısını içerir.

* **agent/prompts.py** – Agent’ın planlama, yürütme ve yorumlama aşamalarında LLM ile etkileşimini yöneten Türkçe system prompt’ları ve mesaj şablonlarını tanımlar.

---

## `ExecutionContext` sınıfı

Nedir?
ExecutionContext, agent’ın analiz süreci boyunca ihtiyaç duyduğu tüm durumsal bilgileri (veri seti, analiz adımları, ara sonuçlar ve önemli bulgular) tek bir yapı altında tutan merkezi bir yürütme bağlamıdır. Agent’ın “hafızası” gibi çalışarak analiz sürecinin bütüncül şekilde izlenmesini sağlar.


Neden Kullanılır?
Çok adımlı analiz süreçlerinde, her adımda elde edilen bilgilerin kaybolmadan saklanması ve sonraki adımlarda tekrar kullanılabilmesi gerekir. ExecutionContext, bu ihtiyacı karşılayarak analiz akışının tutarlı, izlenebilir ve yeniden üretilebilir olmasını sağlar. Ayrıca LLM’e gönderilecek bağlamın dağınık değil, anlamlı ve özetlenmiş bir yapıdan üretilmesini mümkün kılar.


### Ana Fonksiyonlar

#### context.py

##### __init__()

**Amaç:** ExecutionContext nesnesini varsayılan değerlerle başlatarak analiz süreci için boş ve temiz bir yürütme bağlamı oluşturur.

**Parametreler:**

| Parametre | Tip              | Açıklama                                                                      |
|-----------|------------------|-------------------------------------------------------------------------------|
|   -       |      -           | Paramatre almaz                                                               |


**Dönüş Değeri:**

| Alan                | Tip   | Açıklama                     |
|---------------------|-------|------------------------------|
| None                | None  | Geri dönüş değeri yok        |


**Örnek Kullanım - 1: Boş Context Oluşturma**

```python
from memory.context import ExecutionContext

# Yeni ve boş bir execution context oluşturulur
context = ExecutionContext()

```

##### set_dataframe

**Amaç:** Analiz sürecinde kullanılacak pandas DataFrame’i execution context’e ekleyerek, veri setinin yapısal bilgisini (satır–sütun sayısı, sütun isimleri ve veri tipleri) merkezi olarak saklar ve sonraki analiz adımlarının bu bilgilere tutarlı şekilde erişmesini sağlar.

**Parametreler:**

| Parametre | Tip                 | Açıklama                                                                      |
|-----------|---------------------|-------------------------------------------------------------------------------|
|   df      | pandas.DataFrame    | Analiz edilecek veri seti                                                     |


**Dönüş Değeri:**

| Alan                | Tip   | Açıklama                     |
|---------------------|-------|------------------------------|
| None                | None  | Geri dönüş değeri yok        |


**Örnek Kullanım - 1: DataFrame Sonradan Ayarlama**

```python
from memory.context import ExecutionContext
import pandas as pd

context = ExecutionContext()
df = pd.read_csv("data/sample.csv")

context.set_dataframe(df)

```

##### add_step_result

**Amaç:** Bir analiz adımına ait sonucu, adım adı, zaman bilgisi ve çalıştırılma sırası ile birlikte execution context içerisinde saklar.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                  |
|-------------|---------------------|---------------------------|
| step_name   | str                 | Analiz adımının adı       |
| result      | dict                | Adıma ait sonuç verisi    |


**Dönüş Değeri:**

| Alan                | Tip      | Açıklama                     |
|---------------------|----------|------------------------------|
| step_name           | str      | Analiz adımının adı          |
| result              | dict     | Adıma ait sonuç verisi       |
| timestamp           | datetime | Kayıt zamanı                 |
| step_number         | int      | Adımın çalıştırılma sırası   |



**Örnek Kullanım - 1: Analiz Adımı Sonucu Kaydetme**

```python
from memory.context import ExecutionContext

context = ExecutionContext()

context.add_step_result(
    step_name="load_and_inspect",
    result={
        "shape": (100, 3),
        "columns": ["id", "age", "income"]
    }
)
```

**Örnek Kullanım - 2: Çoklu Adım Sonuçlarının Kaydedilmesi**

```python
context.add_step_result(
    step_name="compute_statistics",
    result={
        "mean_age": 35.2,
        "mean_income": 50123
    }
)

# Sonraki adımlarda tüm sonuçlara erişilebilir
# context.step_results
```


##### add_insight

**Amaç:** Analiz sürecinde elde edilen önemli bir bulguyu, önem seviyesi ve zaman bilgisi ile birlikte execution context’e kaydeder.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                                |
|-------------|---------------------|-----------------------------------------|
| text        | str                 | Bulgu metni                             |
| severity    | str                 | Önem seviyesi (info, warning critical)  |


**Dönüş Değeri:**

| Alan                | Tip      | Açıklama                     |
|---------------------|----------|------------------------------|
| text                | str      | Bulgu metni                  |
| severity            | str      | Bulgunun önem seviyesi       |
| timestamp           | datetime | Bulgunun kaydedildiği zaman  |



**Örnek Kullanım - 1: Bilgilendirici Bulgu Ekleme**

```python
from memory.context import ExecutionContext

context = ExecutionContext()

context.add_insight(
    text="Veri seti başarıyla yüklendi",
    severity="info"
)
```

**Örnek Kullanım - 2: Uyarı Seviyesinde Bulgu Ekleme**

```python
context.add_insight(
    text="Age sütununda %20 oranında eksik veri tespit edildi",
    severity="warning"
)

# Eklenen tüm bulgulara erişilebilir
# context.insights
```


##### set_plan

**Amaç:** Agent’ın analiz sürecinde izleyeceği adımları temsil eden mevcut planı execution context içerisinde saklar.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                                   |
|-------------|---------------------|--------------------------------------------|
| plan        | list[dict]          | Analiz planını oluşturan adımların listesi |



**Dönüş Değeri:**

| Alan                | Tip      | Açıklama                     |
|---------------------|----------|------------------------------|
| None                | None     | Geri dönüş değeri yok        |



**Örnek Kullanım - 1: Analiz Planı Tanımlama**

```python
from memory.context import ExecutionContext

context = ExecutionContext()

plan = [
    {"step_number": 1, "action": "load_and_inspect"},
    {"step_number": 2, "action": "compute_statistics"}
]

context.set_plan(plan)
```

**Örnek Kullanım - 2: Planın Sonradan Güncellenmesi**

```python
new_plan = [
    {"step_number": 1, "action": "load_and_inspect"},
    {"step_number": 2, "action": "check_missing"},
    {"step_number": 3, "action": "generate_summary"}
]

context.set_plan(new_plan)
```


##### get_step_result

**Amaç:** Daha önce kaydedilmiş analiz adımları arasından, verilen adım adına (step_name) ait sonucu execution context içinden getirir.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                                           |
|-------------|---------------------|----------------------------------------------------|
| step_name   | str                 | Sonucu alınmak istenen analiz adımının adı         |



**Dönüş Değeri:**

| Alan                | Tip      | Açıklama                                              |
|---------------------|----------|-------------------------------------------------------|
| step_result	      | dict	 |Adıma ait kayıtlı sonuç varsa sonuç dict’i, yoksa None |



**Örnek Kullanım - 1: Mevcut Adım Sonucunu Alma**

```python
result = context.get_step_result("load_and_inspect")

if result is not None:
    print(result)
```

**Örnek Kullanım - 2: Sonuç Bulunamadığında**

```python
result = context.get_step_result("detect_outliers")

if result is None:
    print("Bu adıma ait bir sonuç bulunamadı.")
```


##### get_context_for_llm

**Amaç:** Execution context içerisinde biriken veri özeti, tamamlanan analiz adımları ve önemli bulguları, LLM’in anlayabileceği sade ve yapılandırılmış bir metin haline getirir.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                                           |
|-------------|---------------------|----------------------------------------------------|
|   -         |      -              | Paramatre almaz                                    |



**Dönüş Değeri:**

| Alan                | Tip      | Açıklama                                              |
|---------------------|----------|-------------------------------------------------------|
|context_summary      | str	     |LLM’e gönderilecek formatlanmış context özeti          |



**Örnek Kullanım - 1: LLM’e Gönderilecek Context Oluşturma**

```python

context_text = context.get_context_for_llm()
print(context_text)
```

**Örnek Kullanım - 2: LLM Çağrısı Öncesi Kullanım**

```python

llm_input = context.get_context_for_llm()

# llm_input değişkeni system veya user prompt içine eklenebilir
# llm.generate(llm_input)
```

##### get_completed_steps

**Amaç:** Execution context içerisinde kaydedilmiş analiz adımlarının isimlerini, çalıştırılma sırasına göre bir liste halinde döndürür.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                                             |
|-------------|---------------------|------------------------------------------------------|
|   -         |      -              | Paramatre almaz                                      |



**Dönüş Değeri:**

| Alan                | Tip        | Açıklama                                              |
|---------------------|------------|-------------------------------------------------------|
|completed_steps      |list[str]   |Tamamlanan analiz adımlarının isimleri                 |



**Örnek Kullanım - 1: Tamamlanan Adımları Listeleme**

```python

steps = context.get_completed_steps()
print(steps)
```

**Örnek Kullanım - 2: Belirli Bir Adımın Çalıştırılıp Çalıştırılmadığını Kontrol Etme**

```python

if "compute_statistics" in context.get_completed_steps():
    print("İstatistik adımı tamamlandı.")
```



##### get_insights_by_severity

**Amaç:** Execution context içerisinde kaydedilmiş bulgular arasından, verilen önem seviyesine (severity) sahip olanları filtreleyerek döndürür.

**Parametreler:**

| Parametre   | Tip                 | Açıklama                                              |
|-------------|---------------------|-------------------------------------------------------|
|  severity   |      str            | Filtrelenecek önem seviyesi (info, warning, critical) |




**Dönüş Değeri:**

| Alan                | Tip        | Açıklama                                              |
|---------------------|------------|-------------------------------------------------------|
|insights             |list[dict]  |Belirtilen önem seviyesine sahip bulguların listesi    |



**Örnek Kullanım - 1: Uyarı Seviyesindeki Bulguları Getirme**

```python

warnings = context.get_insights_by_severity("warning")

for w in warnings:
    print(w["text"])
```

**Örnek Kullanım - 2: Kritik Bulguların Kontrolü**

```python

critical_insights = context.get_insights_by_severity("critical")

if critical_insights:
    print("Kritik seviyede bulgular mevcut.")
```



##### clear

**Amaç:** Execution context’i yeni bir analiz süreci için sıfırlayarak, daha önceki veri, plan, adım sonuçları ve bulguları temizler.

**Parametreler:**

| Parametre | Tip              | Açıklama                    |
|-----------|------------------|-----------------------------|
|   -       |      -           | Paramatre almaz             |


**Dönüş Değeri:**

| Alan                | Tip   | Açıklama                     |
|---------------------|-------|------------------------------|
| None                | None  | Geri dönüş değeri yok        |



**Örnek Kullanım - 1: Context’i Temizleme**

```python

context.clear()
```



##### to_dict

**Amaç:** Execution context’in mevcut durumunu, serileştirme (ör. JSON’a çevirme, loglama veya dış sistemlere aktarma) için sözlük (dict) formatında döndürür.

**Parametreler:**

| Parametre | Tip              | Açıklama                                                     |
|-----------|------------------|--------------------------------------------------------------|
|   -       |      -           | Paramatre almaz                                              |


**Dönüş Değeri:**

| Alan                | Tip           | Açıklama                                              |
|---------------------|---------------|-------------------------------------------------------|
|dataframe	          | dict- None    |DataFrame varsa şekil ve sütun bilgileri, yoksa None   |
|metadata	          | dict	      |Veri setine ait meta bilgiler                          |
|step_results	      |list[dict]	  |Kaydedilen analiz adımı sonuçları                      |
|current_plan	      |list[dict]	  |Mevcut analiz planı                                    |
|insights	          |list[dict]	  |Kaydedilen önemli bulgular                             |
|created_at	          |str	          |Context oluşturulma zamanı (ISO format)                |



**Örnek Kullanım - 1: Context’i Dict’e Çevirme**

```python

context_dict = context.to_dict()
print(context_dict)
```

**Örnek Kullanım - 2: Serileştirme Amaçlı Kullanım**

```python

import json

context_json = json.dumps(context.to_dict(), indent=2)
print(context_json)
```



##### __repr__

**Amaç:** ExecutionContext nesnesinin mevcut durumunu, DataFrame bilgisi, tamamlanan adım sayısı ve bulgu sayısını içeren okunabilir bir metin olarak döndürür.

**Parametreler:**

| Parametre | Tip              | Açıklama                                                     |
|-----------|------------------|--------------------------------------------------------------|
|   -       |      -           | Paramatre almaz                                              |


**Dönüş Değeri:**

| Alan                | Tip           | Açıklama                                              |
|---------------------|---------------|-------------------------------------------------------|
|repr	              | str           |Context’in özet durumunu gösteren string               |



**Örnek Kullanım - 1: Context Durumunu Görüntüleme**

```python

print(context)
```

**Örnek Kullanım - 2: Debug Amaçlı Kullanım**

```python

context = ExecutionContext()
print(repr(context))
```
---






## get_context_for_llm() Nasıl Çalışır?

get_context_for_llm() metodu, execution context içerisinde biriken tüm analiz bilgilerini LLM’e gönderilmeye uygun, okunabilir ve yapılandırılmış bir metne dönüştürür. Amaç, LLM’in analiz sürecinin mevcut durumunu tek seferde ve bağlamı kaybetmeden anlayabilmesini sağlamaktır.

Metot, ilk olarak veri setine ait temel bilgileri (satır ve sütun sayısı) metadata üzerinden özetler. Bu sayede LLM, analiz edilen verinin büyüklüğü ve yapısı hakkında hızlıca fikir edinir.

Ardından, tamamlanan analiz adımları sırayla listelenir. Her adım için varsa kısa bir özet bilgi eklenerek, LLM’in analiz sürecinde hangi işlemlerin gerçekleştirildiğini görmesi sağlanır.

Son olarak, analiz sırasında tespit edilen önemli bulgular önem seviyeleriyle birlikte eklenir. Bu yapı, LLM’in hem sonuçları yorumlarken hem de yeni kararlar üretirken kritik noktaları önceliklendirmesine yardımcı olur.

Bu yaklaşım sayesinde LLM’e ham veri veya dağınık bilgiler yerine, anlamlandırılmış ve özetlenmiş bir bağlam sunulur; böylece daha tutarlı ve doğru çıktılar elde edilir.

---

## System promptlar

Bu projede LLM ile etkileşim, farklı sorumluluklara sahip system prompt’lar aracılığıyla yapılandırılmıştır. Her prompt, LLM’e belirli bir rol atayarak analiz sürecinin kontrollü ve tutarlı şekilde ilerlemesini sağlar.

### Planner Prompt Tasarımı
PLANNER_SYSTEM_PROMPT, LLM’i bir veri analiz planlayıcısı rolüne sokar. Bu prompt’un amacı, verilen veri seti bilgilerine dayanarak hangi analiz adımlarının hangi sırayla çalıştırılacağını belirleyen bir plan üretmektir.

Prompt içerisinde:

 * Kullanılabilecek araçlar açıkça listelenmiştir.

 * Analizin mutlaka load_and_inspect ile başlaması ve generate_summary ile bitmesi zorunlu tutulmuştur.

 * Maksimum adım sayısı sınırlandırılarak gereksiz analizlerin önüne geçilmiştir.

 * Üretilen çıktının JSON formatında olması istenmiştir.


```python
{
  "plan": [
    {
      "step_number": 1,
      "action": "load_and_inspect",
      "description": "Veriyi yükle ve yapısını incele",
      "tool": "data_loader"
    },
    {
      "step_number": 2,
      "action": "compute_statistics",
      "description": "Temel istatistikleri hesapla",
      "tool": "statistics"
    }
  ]
}
```
Bu yapı sayesinde agent, LLM’in ürettiği planı doğrudan çalıştırabilir ve ExecutionContext içinde takip edebilir.

### Executor Prompt Tasarımı

EXECUTOR_SYSTEM_PROMPT, LLM’i bir analiz sonuçları yorumlayıcısı rolüne sokar. Bu prompt’un amacı, çalıştırılmış bir analiz adımının çıktısını teknik bilgisi sınırlı kullanıcılar için anlaşılır hale getirmektir.

Executor prompt:

 * Yorumların kısa ve net olmasını,

 * Sayısal değerlerin yorumlanmasını,

 * Eksik veri veya aykırı değer gibi risklerin vurgulanmasını
zorunlu kılar.

```python
# Adım: compute_statistics
# Sonuç: Ortalama yaş 35.2, maksimum yaş 68
```
LLM’den beklenen çıktı:

 + Yaş ortalaması 35 civarındadır ve veri setinde ileri yaşlara sahip gözlemler bulunmaktadır. Bu durum bazı analizlerde aykırı değer etkisi oluşturabilir.

---

### Prompt Engineering Teknikleri

Bu projede prompt’lar, LLM’in belirsiz veya kontrolsüz çıktılar üretmesini engellemek ve analiz sürecini deterministik hale getirmek amacıyla belirli prompt engineering teknikleri kullanılarak tasarlanmıştır.

#### Rol Tabanlı Promptlama (Role Prompting)

Her system prompt’ta LLM’e açık bir rol atanmıştır.
Örneğin PLANNER_SYSTEM_PROMPT, LLM’i bir veri analiz planlayıcısı rolüne sokarken; EXECUTOR_SYSTEM_PROMPT LLM’i bir analiz yorumlayıcısı olarak konumlandırır. Bu yaklaşım, LLM’in hangi bağlamda cevap üretmesi gerektiğini netleştirir.

#### Kural ve Kısıt Tanımlama

Prompt’lar içerisinde açık kurallar tanımlanarak LLM’in davranış alanı sınırlandırılmıştır.
Örneğin:

 * Analizin her zaman load_and_inspect ile başlaması,

 * generate_summary ile bitmesi,

 * Maksimum adım sayısının sınırlandırılması 
 
 gibi kurallar, tutarsız ve gereksiz çıktıları engeller.

#### Yapılandırılmış Çıktı Zorlaması (Structured Output)

Planner prompt’ta LLM’den JSON formatında çıktı üretmesi istenmiştir.
Bu teknik sayesinde LLM çıktıları:

 * makine tarafından kolayca parse edilebilir,

 * doğrudan agent tarafından yürütülebilir,

 * hata yapma olasılığı düşük bir yapıya kavuşur.

#### Açıklayıcı Örneklerle Yönlendirme

Prompt’larda beklenen çıktı formatı ve davranış, örnekler üzerinden gösterilmiştir.
Bu yaklaşım, LLM’in soyut talimatları yanlış yorumlamasını engeller ve çıktı kalitesini artırır.

#### Dil ve Ton Kontrolü

Tüm prompt’larda yanıtların Türkçe olması açıkça belirtilmiştir.
Buna karşın JSON alan adları İngilizce bırakılarak teknik tutarlılık korunmuştur. Bu denge, hem kullanıcı dostu hem de sistem uyumlu çıktılar elde edilmesini sağlar.

#### Kapsam ve Uzunluk Kontrolü

Executor prompt’ta yanıtların 2–3 cümle ile sınırlandırılması istenmiştir.
Bu teknik, LLM’in gereksiz detaylara girmesini engelleyerek kısa, öz ve anlamlı yorumlar üretmesini sağlar.


##### Bu tekniklerin birlikte kullanılması sayesinde:

 * LLM davranışı öngörülebilir hale gelir,

 * Analiz süreci kontrol altında tutulur,

 * Üretilen çıktılar doğrudan kullanıcıya sunulabilecek kaliteye ulaşır.

---

## Şablonlar ve Format Fonksiyonları

Bu projede LLM’e gönderilen mesajların her seferinde aynı düzenle iletilmesi için metin şablonları kullanılmıştır. Böylece LLM’e giden bilgiler dağınık veya rastgele bir metin yerine, neyin nerede olduğu belli olan bir yapı içerisinde sunulmuştur.

Veri seti bilgileri, analiz adımı sonuçları ve özet rapor istekleri için ayrı şablonlar tanımlanmıştır. Bu yaklaşım, LLM’in gönderilen mesajı daha kolay anlamasını ve hangi bilginin ne anlama geldiğini karıştırmamasını sağlar. Aynı zamanda kod içerisinde tekrar eden metin yazımını azaltarak bakım ve güncelleme sürecini kolaylaştırır.

Şablonlar, format_* fonksiyonları aracılığıyla doldurularak dinamik hale getirilmiştir. Böylece hem mesaj içeriği değiştirilebilir tutulmuş hem de LLM ile kurulan iletişim daha kontrollü ve tutarlı bir yapıya kavuşturulmuştur.

---

## Türkçe Çıktı İçin İpuçları


Bu projede üretilen analiz sonuçlarının kullanıcı tarafından doğrudan anlaşılabilmesi amacıyla LLM’den Türkçe çıktı üretmesi özellikle istenmiştir. Prompt’larda dil tercihi açıkça belirtilerek, yorum ve açıklamaların Türkçe olması sağlanmıştır.

Buna karşılık, yapılandırılmış çıktılarda kullanılan JSON alan adları İngilizce bırakılmıştır. Bunun nedeni, bu alanların sistem tarafından işlenen teknik yapılar olması ve programatik uyumluluğun korunmak istenmesidir. Böylece hem makine tarafından kolayca işlenebilen hem de kullanıcıya Türkçe olarak sunulabilen bir çıktı yapısı elde edilmiştir.

Ayrıca prompt’larda kullanılan açık kurallar ve dil yönlendirmeleri, LLM’in gereksiz detaylara girmeden kısa, net ve anlaşılır Türkçe cevaplar üretmesine yardımcı olmuştur.

---

## Öğrenilen Dersler

Bu modül geliştirilirken, analiz sürecinde oluşan tüm bilgilerin merkezi bir yapı (ExecutionContext) altında tutulmasının LLM ile kurulan iletişimi ciddi şekilde sadeleştirdiği görülmüştür. Fonksiyon bazlı ilerleyerek her analiz adımının ayrı ayrı kaydedilmesi, sürecin izlenebilirliğini ve hata ayıklamayı kolaylaştırmıştır.

Ayrıca get_context_for_llm() gibi özetleyici fonksiyonların, LLM’e ham veri yerine anlamlandırılmış bilgi göndermenin çıktı kalitesini artırdığını göstermiştir. Prompt ve context yapısının ayrıştırılması, kodun daha okunabilir ve yönetilebilir olmasını sağlamıştır.

---

## İyileştirme Önerileri

Gelecekte ExecutionContext yapısı kalıcı depolama ile desteklenerek analiz sürecinin disk veya veritabanı üzerinden devam ettirilebilmesi sağlanabilir. Büyük analizlerde context boyutunun artması durumunda, get_context_for_llm() fonksiyonuna otomatik özetleme veya kırpma mekanizması eklenebilir.

Ayrıca farklı agent rollerine göre özelleştirilmiş prompt ve context formatları tanımlanarak sistem daha esnek ve genişletilebilir hale getirilebilir.

---