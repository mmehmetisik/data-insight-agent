"""
planner.py - Plan Oluşturma Modülü
==================================
Görev: Kişi 4 (En deneyimli kişi)
Branch: feature/agent-planner-executor
Zorluk: ⭐⭐⭐⭐ Zor

Bu modül veri analizi için plan oluşturur.
LLM'e veri hakkında bilgi verilir, LLM analiz adımlarını planlar.

Bağımlılıklar:
- agent/prompts.py (sistem promptları)
- memory/context.py (ExecutionContext)
"""

import json
from groq import Groq
from typing import List, Dict, Any, Optional

# Path ayarı - config.py üst klasörde olduğu için sys.path'e ekliyoruz
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Config ayarları
from config import GROQ_API_KEY, PLANNER_MODEL, MODEL_TEMPERATURE, MAX_TOKENS

# Prompts
from agent.prompts import PLANNER_SYSTEM_PROMPT

class Planner:
    """
    Veri analizi için plan oluşturan sınıf.
    
    Görevleri:
    1. Veri hakkında bilgi al (sütunlar, tipler, boyut)
    2. LLM'e bu bilgiyi gönder
    3. LLM'den analiz planı al
    4. Planı yapılandırılmış formata çevir
    """
    
    def __init__(self):
        """
        Planner'ı başlat.
        
        Groq client'ı oluşturur ve model ayarlarını yükler.
        Client bir kere oluşturulur, her çağrıda tekrar bağlantı kurulmaz.
        """
        # Groq client oluştur
        self.client = Groq(api_key=GROQ_API_KEY)
        
        # Model ayarları
        self.model = PLANNER_MODEL
        self.temperature = MODEL_TEMPERATURE
        self.max_tokens = MAX_TOKENS
        
        # Sistem promptu
        self.system_prompt = PLANNER_SYSTEM_PROMPT
    
    def create_plan(self, data_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Veri bilgisine göre analiz planı oluştur.
        
        Args:
            data_info: Veri hakkında bilgiler
                - shape: (satır, sütun) tuple
                - columns: sütun isimleri listesi
                - dtypes: sütun tipleri dict
                - missing: eksik veri bilgisi dict
        
        Returns:
            Plan listesi, her adım için:
                - step_number: Adım numarası
                - action: Yapılacak işlem
                - description: Türkçe açıklama
                - tool: Kullanılacak araç
        """
        # Veri bilgisini LLM için formatla
        formatted_data = self._format_data_info(data_info)
        
        # Kullanıcı promptu oluştur
        user_prompt = f"""Aşağıdaki veri seti için analiz planı oluştur:

{formatted_data}

Planı JSON formatında döndür."""
        
        # LLM'e istek gönder ve cevap al
        llm_response = self._call_llm(user_prompt)
        
        # LLM cevabını parse edip plan listesine çevir
        plan = self._parse_plan(llm_response)
        
        return plan
    
    def _format_data_info(self, data_info: Dict[str, Any]) -> str:
        """
        Veri bilgisini LLM'e gönderilecek string formatına çevir.
        
        Args:
            data_info: Veri hakkında bilgiler
        
        Returns:
            Formatlanmış string
        """
        rows, cols = data_info.get('shape', (0, 0))
        columns = data_info.get('columns', [])
        dtypes = data_info.get('dtypes', {})
        missing = data_info.get('missing', {})
        
        # Sütun bilgilerini formatla
        columns_info = []
        for col in columns:
            dtype = dtypes.get(col, 'unknown')
            missing_count = missing.get(col, 0)
            
            if missing_count > 0:
                columns_info.append(f"- {col}: {dtype} ({missing_count} eksik)")
            else:
                columns_info.append(f"- {col}: {dtype}")
        
        # Formatlanmış string oluştur
        formatted = f"""Veri Seti Bilgisi:
-----------------
Boyut: {rows} satır, {cols} sütun

Sütunlar ve Tipleri:
{chr(10).join(columns_info)}

Eksik Veri Özeti:
Toplam {sum(missing.values())} eksik değer, {len(missing)} sütunda dağılmış.
"""
        
        return formatted
    
    def _call_llm(self, prompt: str) -> str:
        """
        LLM'i çağır ve cevap al.
        
        Args:
            prompt: Kullanıcı promptu
        
        Returns:
            LLM'in cevabı
        
        Raises:
            Exception: LLM çağrısı başarısız olursa
        """
        try:
            # Groq API'ye istek gönder
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Cevabı al ve döndür
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"LLM çağrısı başarısız: {str(e)}")
    
    def _parse_plan(self, llm_response: str) -> List[Dict[str, Any]]:
        """
        LLM cevabını plan listesine çevir.
        
        Args:
            llm_response: LLM'den gelen JSON string
        
        Returns:
            Plan listesi
        
        Raises:
            Exception: JSON parse edilemezse veya format geçersizse
        """
        try:
            # JSON parse et - LLM bazen öncesinde/sonrasında metin ekler
            cleaned = llm_response.strip()

            # ``json varsa, sadece o kısmı al
            if "```json" in cleaned:
                start = cleaned.find("```json") + 7
                end = cleaned.find("```", start)
                if end != -1:
                    cleaned = cleaned[start:end].strip()
            elif "```" in cleaned:
                start = cleaned.find("```") + 3
                end = cleaned.find("```", start)
                if end != -1:
                    cleaned = cleaned[start:end].strip()
        
            # JSON'dan dict'e çevir
            parsed = json.loads(cleaned)
            
            # "plan" anahtarını al
            if "plan" in parsed:
                plan = parsed["plan"]
            else:
                # Eğer direkt liste dönmüşse
                plan = parsed if isinstance(parsed, list) else []
            
            # Her adımı doğrula (gerekli anahtarlar var mı?)
            validated_plan = []
            for step in plan:
                if all(key in step for key in ["step_number", "action", "description", "tool"]):
                    validated_plan.append(step)
                else:
                    print(f"⚠️ Geçersiz adım atlandı: {step}")
            
            return validated_plan
            
        except json.JSONDecodeError as e:
            raise Exception(f"Plan JSON parse edilemedi: {str(e)}\nLLM Cevabı: {llm_response[:200]}")
        except Exception as e:
            raise Exception(f"Plan işlenirken hata: {str(e)}")
    
    def revise_plan(self, current_plan: List[Dict], 
                    step_results: List[Dict], 
                    insight: str) -> List[Dict[str, Any]]:
        """
        Bir bulguya göre planı revize et.
        
        Args:
            current_plan: Mevcut plan
            step_results: Şimdiye kadar ki adım sonuçları
            insight: Yeni bulgu (örn: "%40 eksik veri bulundu")
        
        Returns:
            Revize edilmiş plan
        
        Not: Bu metod opsiyoneldir (bonus). 
        Temel implementasyon için sadece create_plan yeterlidir.
        """
        # BONUS TODO: Opsiyonel - Plan revizyonu implementasyonu
        pass


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Planner Test ===\n")
    
    # Test için örnek veri bilgisi (Titanic dataset)
    test_data_info = {
        "shape": (891, 12),
        "columns": ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", 
                    "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"],
        "dtypes": {
            "PassengerId": "int64",
            "Survived": "int64",
            "Pclass": "int64",
            "Name": "object",
            "Sex": "object",
            "Age": "float64",
            "SibSp": "int64",
            "Parch": "int64",
            "Ticket": "object",
            "Fare": "float64",
            "Cabin": "object",
            "Embarked": "object"
        },
        "missing": {
            "Age": 177,
            "Cabin": 687,
            "Embarked": 2
        }
    }
    
    # Planner oluştur
    planner = Planner()
    
    # Plan oluştur (LLM'e istek gönderilecek)
    print("📋 Plan oluşturuluyor... (LLM'e istek gönderiliyor)\n")
    
    try:
        plan = planner.create_plan(test_data_info)
        
        # Planı ekrana yazdır
        print("✅ Oluşturulan Plan:")
        for step in plan:
            print(f"  Adım {step['step_number']}: {step['description']}")
        
        print(f"\n📊 Toplam {len(plan)} adım planlandı.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
