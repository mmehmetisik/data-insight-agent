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

# TODO: Import'ları tamamla
# from config import GROQ_API_KEY, EXECUTOR_MODEL
# from .prompts import EXECUTOR_SYSTEM_PROMPT
# from memory.context import ExecutionContext
# from tools.data_loader import load_and_inspect
# from tools.statistics import compute_statistics
# from tools.analysis import find_correlations, detect_outliers, check_missing
# from tools.reporter import generate_summary


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
        
        TODO:
        1. Groq client oluştur
        2. Araç registry'sini oluştur
        """
        # TODO: Groq client
        # self.client = Groq(api_key=GROQ_API_KEY)
        
        # TODO: Araç registry - her action için hangi fonksiyon çağrılacak
        # self.tool_registry = {
        #     "load_and_inspect": load_and_inspect,
        #     "compute_statistics": compute_statistics,
        #     "check_missing": check_missing,
        #     "find_correlations": find_correlations,
        #     "detect_outliers": detect_outliers,
        #     "generate_summary": generate_summary,
        # }
        pass
    
    def execute_plan(self, plan: List[Dict], context: Any) -> Generator[Dict, None, None]:
        """
        Planı adım adım yürüt ve sonuçları yield et.
        
        Args:
            plan: Planner'dan gelen plan listesi
            context: ExecutionContext objesi
        
        Yields:
            Her adım için:
                - step_number: Adım numarası
                - total_steps: Toplam adım sayısı
                - action: Yapılan işlem
                - description: Açıklama
                - result: İşlem sonucu
                - interpretation: LLM'in yorumu
                - status: "success" veya "error"
        
        Örnek kullanım:
        ```python
        for step_result in executor.execute_plan(plan, context):
            print(f"Adım {step_result['step_number']}: {step_result['status']}")
            print(f"Sonuç: {step_result['result']}")
            print(f"Yorum: {step_result['interpretation']}")
        ```
        
        TODO:
        1. Plan üzerinde döngü kur
        2. Her adım için uygun aracı çağır
        3. Sonucu context'e kaydet
        4. LLM ile yorumla
        5. Sonucu yield et
        """
        # TODO: Implement this method
        
        # Örnek yield yapısı (gerçek implementasyonda doldurulacak):
        # for i, step in enumerate(plan):
        #     # Aracı çağır
        #     tool_func = self.tool_registry.get(step["action"])
        #     result = tool_func(context)
        #     
        #     # Context'e kaydet
        #     context.add_step_result(step["action"], result)
        #     
        #     # Yorumla
        #     interpretation = self._interpret_result(step, result, context)
        #     
        #     # Yield et
        #     yield {
        #         "step_number": i + 1,
        #         "total_steps": len(plan),
        #         "action": step["action"],
        #         "description": step["description"],
        #         "result": result,
        #         "interpretation": interpretation,
        #         "status": "success"
        #     }
        pass
    
    def _execute_step(self, step: Dict, context: Any) -> Dict[str, Any]:
        """
        Tek bir adımı yürüt.
        
        Args:
            step: Plan adımı
            context: ExecutionContext
        
        Returns:
            Adım sonucu
        
        TODO:
        1. Adımdaki action'a göre aracı bul
        2. Aracı çağır
        3. Sonucu döndür
        4. Hata varsa yakala ve döndür
        """
        # TODO: Implement this method
        pass
    
    def _interpret_result(self, step: Dict, result: Dict, context: Any) -> str:
        """
        Adım sonucunu LLM ile yorumla.
        
        Args:
            step: Yapılan adım
            result: Adım sonucu
            context: Mevcut context (geçmiş adımlar dahil)
        
        Returns:
            Türkçe yorum string'i
        
        Örnek yorum:
        "Veri setinde 891 satır ve 12 sütun bulunmaktadır. 
        Age sütununda %20 oranında eksik veri tespit edilmiştir, 
        bu durum analiz sonuçlarını etkileyebilir."
        
        TODO:
        1. Sonucu LLM'e gönder
        2. Türkçe yorum iste
        3. Yorumu döndür
        """
        # TODO: Implement this method
        pass
    
    def _call_llm(self, prompt: str) -> str:
        """
        LLM'i çağır.
        
        Args:
            prompt: Kullanıcı promptu
        
        Returns:
            LLM cevabı
        """
        # TODO: Implement this method
        pass


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
    # from memory.context import ExecutionContext
    # context = ExecutionContext()
    # context.dataframe = pd.read_csv("data/sample_data.csv")
    # 
    # for step_result in executor.execute_plan(test_plan, context):
    #     print(f"Adım {step_result['step_number']}/{step_result['total_steps']}")
    #     print(f"  İşlem: {step_result['description']}")
    #     print(f"  Durum: {step_result['status']}")
    #     print(f"  Yorum: {step_result['interpretation']}")
    #     print()
    
    print("Executor TODO - Henüz implement edilmedi")
    print("\nBeklenen çıktı örneği:")
    print("  Adım 1/3 - Veriyi yükle ve yapısını incele")
    print("    Durum: success")
    print("    Yorum: Veri seti 891 satır ve 12 sütun içeriyor...")
