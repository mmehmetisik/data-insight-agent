"""
executor.py - Plan Yürütme Modülü
=================================
Görev: Kişi 4 (En deneyimli kişi)
Branch: feature/agent-planner-executor
Zorluk: ⭐⭐⭐⭐ Zor

Bu modül oluşturulan planı adım adım yürütür.
Her adımda uygun aracı çağırır ve sonucu context'e kaydeder.

Bağımlılıklar:
- agent/prompts.py (sistem promptları)
- memory/context.py (ExecutionContext)
- tools/* (tüm araçlar)
"""

from typing import Dict, Any, Generator, List
from groq import Groq

# Path ayarı (config.py üst klasörde)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Config ve prompts
from config import GROQ_API_KEY, EXECUTOR_MODEL, MODEL_TEMPERATURE, MAX_TOKENS
from agent.prompts import EXECUTOR_SYSTEM_PROMPT

# Memory
from memory.context import ExecutionContext

# Tools
from tools.data_loader import load_and_inspect
from tools.statistics import compute_statistics
from tools.analysis import find_correlations, detect_outliers, check_missing
from tools.reporter import generate_summary


class Executor:
    """
    Planı adım adım yürüten sınıf.
    
    Görevleri:
    1. Planı al
    2. Her adımı sırayla yürüt
    3. Her adımın sonucunu context'e kaydet
    4. Sonuçları yorumla (LLM ile)
    5. İlerlemeyi yield et (Streamlit için)
    """
    
    def __init__(self):
        """
        Executor'ı başlat.
        
        Groq client oluşturur ve tool rgistry'sini hazırlar.
        """
        # Groq client oluştur
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = EXECUTOR_MODEL
        self.temperature = MODEL_TEMPERATURE
        self.max_tokens = MAX_TOKENS

        # Sistem promptu
        self.system_prompt = EXECUTOR_SYSTEM_PROMPT

        # Tool registry - her action için hangi fonksiyon çağrılacak
        self.tool_registry = {
            "load_and_inspect": load_and_inspect,
            "compute_statistics": compute_statistics,
            "check_missing": check_missing,
            "find_correlations": find_correlations,
            "detect_outliers": detect_outliers,
            "generate_summary": generate_summary,
        }
    
    def execute_plan(self, plan: List[Dict], context: Any) -> Generator[Dict, None, None]:
        """
        Planı adım adım yürüt ve sonuçları yield et.
        """
        total_steps = len(plan)
    
        # Plan üzerinde döngü kur
        for i, step in enumerate(plan):
            try:
                # Adımı yürüt
                result = self._execute_step(step, context)
            
                # Hata kontrolü
                if "error" in result:
                    yield {
                        "step_number": i + 1,
                        "total_steps": total_steps,
                        "action": step["action"],
                        "description": step["description"],
                        "result": result,
                        "interpretation": f"Hata: {result['error']}",
                        "status": "error"
                    }
                    continue
            
                # Context'e kaydet
                context.add_step_result(step["action"], result)
            
                # LLM ile yorumla
                interpretation = self._interpret_result(step, result, context)
            
                # Sonucu yield et
                yield {
                    "step_number": i + 1,
                    "total_steps": total_steps,
                    "action": step["action"],
                    "description": step["description"],
                    "result": result,
                    "interpretation": interpretation,
                    "status": "success"
                }
            
            except Exception as e:
                yield {
                    "step_number": i + 1,
                    "total_steps": total_steps,
                    "action": step.get("action", "unknown"),
                    "description": step.get("description", ""),
                    "result": {"error": str(e)},
                    "interpretation": f"Beklenmeyen hata: {str(e)}",
                    "status": "error"
                }
        
    
    def _execute_step(self, step: Dict, context: Any) -> Dict[str, Any]:
        """
        Tek bir adımı yürüt.
        """
        try:
            # Adımdaki action'a göre aracı bul
            action = step.get("action")
            tool_func = self.tool_registry.get(action)
        
            if not tool_func:
                raise Exception(f"Bilinmeyen action: {action}")
        
            # Aracı çağır
            result = tool_func(context)
        
            return result
        
        except Exception as e:
            return {
                "error": str(e),
                "action": step.get("action"),
                "status": "failed"
            }
    
    def _interpret_result(self, step: Dict, result: Dict, context: Any) -> str:
        """
        Adım sonucunu LLM ile yorumla.
        """
        # Sonucu string formatına çevir
        result_str = str(result)
    
        # LLM'e gönderilecek prompt
        prompt = f"""Adım: {step['description']}
    İşlem: {step['action']}

    Sonuç:
    {result_str}

    Bu sonucu 2-3 cümle ile Türkçe yorumla. Önemli bulguları vurgula."""
    
        # LLM'den yorum al
        interpretation = self._call_llm(prompt)
    
        return interpretation
        
    
    def _call_llm(self, prompt: str) -> str:
        """
        LLM'i çağır.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"LLM çağrısı başarısız: {str(e)}")
        

# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Executor Test ===\n")
    
    # Test için örnek plan
    test_plan = [
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
        },
        {
            "step_number": 3,
            "action": "check_missing",
            "description": "Eksik değerleri analiz et",
            "tool": "analysis"
        },
    ]
    
    # Executor oluştur
    executor = Executor()
    
    # TODO: Test çalıştırma
    from memory.context import ExecutionContext
    import pandas as pd

    context = ExecutionContext()
    context.dataframe = pd.read_csv("data/sample_data.csv")
     
    for step_result in executor.execute_plan(test_plan, context):
        print(f"Adım {step_result['step_number']}/{step_result['total_steps']}")
        print(f"  İşlem: {step_result['description']}")
        print(f"  Durum: {step_result['status']}")
        print(f"  Yorum: {step_result['interpretation']}")
        print()
    

