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

# TODO: config.py'dan ayarları import et
# from config import GROQ_API_KEY, PLANNER_MODEL, MODEL_TEMPERATURE, MAX_TOKENS

# TODO: prompts.py'dan sistem promptunu import et
# from .prompts import PLANNER_SYSTEM_PROMPT


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
        
        TODO:
        1. Groq client'ı oluştur
        2. Model ayarlarını yükle
        """
        # TODO: Groq client oluştur
        # self.client = Groq(api_key=GROQ_API_KEY)
        # self.model = PLANNER_MODEL
        pass
    
    def create_plan(self, data_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Veri bilgisine göre analiz planı oluştur.
        
        Args:
            data_info: Veri hakkında bilgiler
                - shape: (satır, sütun) tuple
                - columns: sütun isimleri listesi
                - dtypes: sütun tipleri dict
                - sample: örnek veriler
        
        Returns:
            Plan listesi, her adım için:
                - step_number: Adım numarası
                - action: Yapılacak işlem (load_data, compute_stats, vb.)
                - description: Türkçe açıklama
                - tool: Kullanılacak araç
        
        Örnek çıktı:
        [
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
            ...
        ]
        
        TODO:
        1. data_info'yu string formatına çevir
        2. LLM'e sistem promptu ve data_info gönder
        3. LLM'den gelen cevabı JSON olarak parse et
        4. Plan listesi olarak döndür
        """
        # TODO: Implement this method
        pass
    
    def _format_data_info(self, data_info: Dict[str, Any]) -> str:
        """
        Veri bilgisini LLM'e gönderilecek string formatına çevir.
        
        Args:
            data_info: Veri hakkında bilgiler
        
        Returns:
            Formatlanmış string
        
        TODO:
        1. Shape bilgisini ekle
        2. Sütun isimlerini ve tiplerini ekle
        3. Örnek veriyi ekle (ilk birkaç satır)
        """
        # TODO: Implement this method
        pass
    
    def _call_llm(self, prompt: str) -> str:
        """
        LLM'i çağır ve cevap al.
        
        Args:
            prompt: Kullanıcı promptu
        
        Returns:
            LLM'in cevabı
        
        TODO:
        1. Groq API'yi çağır
        2. Sistem promptu + kullanıcı promptu gönder
        3. Cevabı döndür
        """
        # TODO: Implement this method
        pass
    
    def _parse_plan(self, llm_response: str) -> List[Dict[str, Any]]:
        """
        LLM cevabını plan listesine çevir.
        
        Args:
            llm_response: LLM'den gelen JSON string
        
        Returns:
            Plan listesi
        
        TODO:
        1. JSON'ı parse et
        2. Her adımı doğrula
        3. Liste olarak döndür
        """
        # TODO: Implement this method
        pass
    
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
        
        Bu metod opsiyoneldir. Temel implementasyon için
        sadece create_plan yeterlidir.
        
        TODO (Opsiyonel - Bonus):
        1. Mevcut durumu LLM'e anlat
        2. Yeni bulguyu paylaş
        3. Revize plan iste
        """
        # TODO: Implement this method (OPTIONAL)
        pass


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== Planner Test ===\n")
    
    # Test için örnek veri bilgisi
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
    
    # Planner oluştur ve test et
    planner = Planner()
    
    # TODO: Test çalıştırma
    # plan = planner.create_plan(test_data_info)
    # print("Oluşturulan Plan:")
    # for step in plan:
    #     print(f"  Adım {step['step_number']}: {step['description']}")
    
    print("Planner TODO - Henüz implement edilmedi")
    print("\nBeklenen çıktı örneği:")
    print("  Adım 1: Veriyi yükle ve yapısını incele")
    print("  Adım 2: Temel istatistikleri hesapla")
    print("  Adım 3: Eksik değerleri analiz et")
    print("  Adım 4: Korelasyonları bul")
    print("  Adım 5: Özet rapor oluştur")
