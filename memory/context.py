
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional


class ExecutionContext:
    """
    Agent'ın yürütme bağlamını (execution context) yöneten sınıf.
    
    Bu sınıf:
    1. DataFrame'i saklar
    2. Her adımın sonucunu kaydeder
    3. Önemli bulguları (insights) toplar
    4. Mevcut planı takip eder
    5. LLM'e gönderilecek özeti oluşturur
    
    Attributes:
        dataframe: Analiz edilen pandas DataFrame
        metadata: Veri hakkında meta bilgiler
        step_results: Her adımın sonucu
        current_plan: Mevcut analiz planı
        insights: Önemli bulgular listesi
        created_at: Context oluşturulma zamanı
    """
    
    def __init__(self):
        """
        ExecutionContext'i başlat.
        1. dataframe = None
        2. metadata = boş dict
        3. step_results = boş liste
        4. current_plan = boş liste
        5. insights = boş liste
        6. created_at = şimdiki zaman
        """
       
        # self.dataframe: Optional[pd.DataFrame] = None
        # self.metadata: Dict[str, Any] = {}
        # self.step_results: List[Dict[str, Any]] = []
        # self.current_plan: List[Dict[str, Any]] = []
        # self.insights: List[Dict[str, Any]] = []
        # self.created_at: datetime = datetime.now()

        self.dataframe: Optional[pd.DataFrame] = None
        self.metadata: Dict[str, Any] = {}
        self.step_results: List[Dict[str, Any]] = []
        self.current_plan: List[Dict[str, Any]] = []
        self.insights: List[Dict[str, Any]] = []
        self.created_at: datetime = datetime.now()
        
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """
        DataFrame'i ayarla ve metadata'yı güncelle.
        
        Args:
            df: pandas DataFrame
        
        1. self.dataframe = df
        2. metadata'yı güncelle (shape, columns, dtypes)
        """
        
        self.dataframe = df
        self.metadata["shape"] = df.shape
        self.metadata["columns"] = list(df.columns)
        self.metadata["dtypes"] = df.dtypes.astype(str).to_dict()
        
    
    def add_step_result(self, step_name: str, result: Dict[str, Any]) -> None:
        """

        Bir adımın sonucunu kaydet.
        
        Args:
            step_name: Adım adı (örn: "load_and_inspect")
            result: Adım sonucu (dict)
        
        Kaydedilecek bilgiler:
            - step_name: adım adı
            - result: sonuç dict'i
            - timestamp: kayıt zamanı
            - step_number: kaçıncı adım
        
        
        1. Yeni sonuç dict'i oluştur
        2. step_results listesine ekle
        """
        

        # step_record = {
        #     "step_name": step_name,
        #     "result": result,
        #     "timestamp": datetime.now(),
        #     "step_number": len(self.step_results) + 1
        # }
        # self.step_results.append(step_record)
        step_record = {
        "step_name": step_name,
        "result": result,
        "timestamp": datetime.now(),
        "step_number": len(self.step_results) + 1
         }

        self.step_results.append(step_record)
    
    
    def add_insight(self, text: str, severity: str = "info") -> None:
        """
        Önemli bir bulgu ekle.
        
        Args:
            text: Bulgu metni
            severity: Önem seviyesi ("info", "warning", "critical")
        
        Örnek:
            context.add_insight("Age sütununda %20 eksik veri", "warning")
        

        1. Insight dict'i oluştur
        2. insights listesine ekle
        """
        # TODO: Implement this method
        insight = {
        "text": text,
        "severity": severity,
        "timestamp": datetime.now()
         }

        self.insights.append(insight)

    
    def set_plan(self, plan: List[Dict[str, Any]]) -> None:
        """
        Mevcut planı ayarla.
        
        Args:
            plan: Plan adımları listesi
        
        
        1. self.current_plan = plan
        """
        
        self.current_plan = plan

    
    def get_step_result(self, step_name: str) -> Optional[Dict[str, Any]]:
        """
        Belirli bir adımın sonucunu getir.
        
        Args:
            step_name: Adım adı
        
        Returns:
            Adım sonucu veya None
        
    
        1. step_results içinde ara
        2. Bulursan döndür, bulamazsan None
        """
        
        for step in self.step_results:
         if step.get("step_name") == step_name:
            return step

        return None
        
    
    def get_context_for_llm(self) -> str:
        """
        LLM'e gönderilecek context özetini oluştur.
        
        Bu metod tüm geçmiş adımları ve bulguları
        LLM'in anlayacağı formatta özetler.
        
        Returns:
            str: LLM için formatlanmış context özeti
        
        Örnek çıktı:
        '''
        === MEVCUT DURUM ===
        
        Veri: 891 satır, 12 sütun
        
        Tamamlanan Adımlar:
        1. load_and_inspect: Veri yüklendi, 12 sütun tespit edildi
        2. compute_statistics: Ortalama yaş 29.7
        
        Önemli Bulgular:
        - [WARNING] Age sütununda %20 eksik veri
        - [INFO] Fare ve Pclass arasında güçlü korelasyon
        '''
        
        
        1. Metadata'yı formatla
        2. Tamamlanan adımları listele
        3. Insights'ları ekle
        4. String olarak döndür
        """
        
        lines = []

        # Başlık
        lines.append("=== MEVCUT DURUM ===\n")

        # Metadata (veri özeti)
        if self.metadata:
            shape = self.metadata.get("shape")
            if shape:
                lines.append(f"Veri: {shape[0]} satır, {shape[1]} sütun\n")

        # Tamamlanan adımlar
        if self.step_results:
            lines.append("Tamamlanan Adımlar:")
            for step in self.step_results:
                step_name = step.get("step_name")
                result = step.get("result", {})
                summary = result.get("summary") or result.get("message") or ""
                lines.append(f"- {step_name}: {summary}")
            lines.append("")  # boş satır

        # Önemli bulgular
        if self.insights:
            lines.append("Önemli Bulgular:")
            for insight in self.insights:
                severity = insight.get("severity", "info").upper()
                text = insight.get("text", "")
                lines.append(f"- [{severity}] {text}")

        return "\n".join(lines)
    
    
    def get_completed_steps(self) -> List[str]:
        """
        Tamamlanan adımların isimlerini döndür.
        
        Returns:
            List[str]: Adım isimleri
        """
        # TODO: Implement this method
        # return [step["step_name"] for step in self.step_results]
        return [step["step_name"] for step in self.step_results]
        
    
    def get_insights_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """
        Belirli seviyedeki bulguları getir.
        
        Args:
            severity: "info", "warning", veya "critical"
        
        Returns:
            List: Filtrelenmiş bulgular
        """
        # TODO: Implement this method
        return [
        insight
        for insight in self.insights
        if insight.get("severity") == severity
        ]
        
    
    def clear(self) -> None:
        """
        Context'i sıfırla (yeni analiz için).
        
        
        1. Tüm listeleri temizle
        2. dataframe = None
        3. metadata = boş dict
        """
        
        self.dataframe = None
        self.metadata = {}
        self.step_results = []
        self.current_plan = []
        self.insights = []
        self.created_at = datetime.now()
       
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Context'i dict olarak döndür (serialize için).
        
        Returns:
            Dict: Tüm context bilgisi
        """
        
        return {
        "dataframe": {
            "shape": self.dataframe.shape,
            "columns": list(self.dataframe.columns)
        } if self.dataframe is not None else None,
        "metadata": self.metadata,
        "step_results": self.step_results,
        "current_plan": self.current_plan,
        "insights": self.insights,
        "created_at": self.created_at.isoformat()
        }
        
    
    def __repr__(self) -> str:
        """String representation"""
        df_info = f"{self.dataframe.shape}" if self.dataframe is not None else "None"
        return f"ExecutionContext(df={df_info}, steps={len(self.step_results)}, insights={len(self.insights)})"


# =============================================================================
# TEST KODU
# =============================================================================

if __name__ == "__main__":
    print("=== ExecutionContext Test ===\n")
    
    import numpy as np
    
    # Test DataFrame
    test_df = pd.DataFrame({
        'id': range(1, 101),
        'age': np.random.normal(35, 10, 100),
        'income': np.random.normal(50000, 15000, 100)
    })
    
    # Context oluştur
    context = ExecutionContext()
    
    # Test: set_dataframe
    print("--- set_dataframe() testi ---")
    context.set_dataframe(test_df)
    print(f"DataFrame shape: {context.dataframe.shape if context.dataframe is not None else 'TODO'}")
    print()
    
    # Test: add_step_result
    print("--- add_step_result() testi ---")
    context.add_step_result("load_and_inspect", {
        "shape": (100, 3),
        "columns": ["id", "age", "income"]
    })
    context.add_step_result("compute_statistics", {
        "mean_age": 35.2,
        "mean_income": 50123
    })
    print(f"Step results count: {len(context.step_results) if hasattr(context, 'step_results') and context.step_results else 'TODO'}")
    print()
    
    # Test: add_insight
    print("--- add_insight() testi ---")
    context.add_insight("Veri setinde 100 satır var", "info")
    context.add_insight("Income sütununda outlier var", "warning")
    print(f"Insights count: {len(context.insights) if hasattr(context, 'insights') and context.insights else 'TODO'}")
    print()
    
    # Test: get_context_for_llm
    print("--- get_context_for_llm() testi ---")
    llm_context = context.get_context_for_llm()
    if llm_context:
        print(llm_context[:300] + "...")
    else:
        print("TODO: get_context_for_llm() henüz implement edilmedi")
    print()
    
    # Test: __repr__
    print("--- __repr__() testi ---")
    print(f"Context: {context}")
    
    print("\n=== Test Tamamlandı ===")
