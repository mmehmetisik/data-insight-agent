"""
app.py - Streamlit Ana Uygulaması
=================================
Görev: Team Lead (Mehmet)
Durum: İSKELET - Tüm parçalar hazır olunca tamamlanacak

Bu dosya Streamlit web arayüzünü oluşturur.
Diğer tüm parçalar (planner, executor, tools, context) 
hazır olduktan sonra Team Lead tarafından entegre edilecek.

Çalıştırma:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd

# TODO: Tüm importları tamamla (diğer modüller hazır olunca)
# from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT, PREVIEW_ROWS
# from agent.planner import Planner
# from agent.executor import Executor
# from memory.context import ExecutionContext

# =============================================================================
# SAYFA AYARLARI
# =============================================================================

st.set_page_config(
    page_title="📊 Data Insight Agent",
    page_icon="📊",
    layout="wide"
)

# =============================================================================
# ANA SAYFA
# =============================================================================

st.title("📊 Data Insight Agent")
st.markdown("*AI destekli otomatik veri analizi*")

# =============================================================================
# SIDEBAR - VERİ YÜKLEME
# =============================================================================

with st.sidebar:
    st.header("📁 Veri Kaynağı")
    
    data_source = st.radio(
        "Kaynak seçin:",
        ["Dosya Yükle", "Örnek Veri"]
    )
    
    df = None
    
    if data_source == "Dosya Yükle":
        uploaded_file = st.file_uploader(
            "CSV dosyası yükleyin",
            type=["csv"]
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ {uploaded_file.name} yüklendi!")
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
    
    else:  # Örnek Veri
        sample_options = ["Titanic", "Iris", "Tips"]
        selected_sample = st.selectbox("Örnek veri seçin:", sample_options)
        
        # TODO: Örnek veri setlerini yükle
        # if selected_sample == "Titanic":
        #     df = pd.read_csv("data/titanic.csv")
        # elif selected_sample == "Iris":
        #     df = pd.read_csv("data/iris.csv")
        
        st.info("💡 Örnek veri setleri yakında eklenecek")
    
    st.divider()
    
    # Grafik seçenekleri
    st.header("📊 Grafik Seçenekleri")
    show_correlation = st.checkbox("Korelasyon Haritası", value=True)
    show_missing = st.checkbox("Eksik Veri Grafiği", value=True)
    show_distribution = st.checkbox("Dağılım Grafikleri", value=False)

# =============================================================================
# ANA ALAN
# =============================================================================

if df is not None:
    # Veri Önizleme
    st.subheader("📋 Veri Önizleme")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Satır Sayısı", df.shape[0])
    with col2:
        st.metric("Sütun Sayısı", df.shape[1])
    with col3:
        st.metric("Eksik Değer", df.isnull().sum().sum())
    
    st.dataframe(df.head(10), use_container_width=True)
    
    st.divider()
    
    # Analiz Başlat Butonu
    if st.button("🚀 Analizi Başlat", type="primary", use_container_width=True):
        
        # TODO: Bu kısım tüm modüller hazır olunca tamamlanacak
        
        st.subheader("📝 Analiz Planı")
        
        # Placeholder plan (gerçek plan Planner'dan gelecek)
        placeholder_plan = [
            "Veriyi yükle ve yapısını incele",
            "Temel istatistikleri hesapla",
            "Eksik değerleri analiz et",
            "Korelasyonları bul",
            "Aykırı değerleri tespit et",
            "Özet rapor oluştur"
        ]
        
        for i, step in enumerate(placeholder_plan, 1):
            st.write(f"**Adım {i}:** {step}")
        
        st.divider()
        
        # Yürütme simülasyonu
        st.subheader("⚙️ Yürütme")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # TODO: Gerçek executor ile değiştir
        # for step_result in executor.execute_plan(plan, context):
        #     progress_bar.progress(step_result["step"] / step_result["total"])
        #     with st.expander(f"✅ Adım {step_result['step']}: {step_result['description']}"):
        #         st.json(step_result["result"])
        #         st.markdown(f"**Yorum:** {step_result['interpretation']}")
        
        import time
        for i, step in enumerate(placeholder_plan, 1):
            progress_bar.progress(i / len(placeholder_plan))
            status_text.text(f"İşleniyor: {step}...")
            time.sleep(0.5)  # Simülasyon için bekleme
            
            with st.expander(f"✅ Adım {i}: {step}", expanded=(i == len(placeholder_plan))):
                st.info("🔧 Bu adımın sonucu, ilgili modül tamamlandığında gösterilecek.")
        
        status_text.text("✅ Analiz tamamlandı!")
        
        st.divider()
        
        # Final Rapor (Placeholder)
        st.subheader("📊 Final Rapor")
        
        st.markdown("""
        ## 📊 Veri Analiz Raporu
        
        *Bu rapor, tüm modüller tamamlandığında otomatik oluşturulacaktır.*
        
        ### Genel Bakış
        - Veri seti başarıyla yüklendi
        - Temel analizler tamamlandı
        
        ### Sonraki Adımlar
        - [ ] Planner modülünü tamamla
        - [ ] Executor modülünü tamamla
        - [ ] Tools modüllerini tamamla
        - [ ] Grafikleri ekle
        """)
        
        # Rapor indirme butonu (placeholder)
        st.download_button(
            label="📥 Raporu İndir (MD)",
            data="# Placeholder Rapor\n\nGerçek rapor yakında...",
            file_name="analiz_raporu.md",
            mime="text/markdown"
        )

else:
    # Veri yüklenmemişse
    st.info("👈 Sol taraftan bir veri kaynağı seçin veya CSV dosyası yükleyin.")
    
    st.markdown("""
    ### 🎯 Bu Uygulama Ne Yapar?
    
    1. **CSV dosyanızı yükleyin** veya örnek veri seçin
    2. **"Analizi Başlat"** butonuna tıklayın
    3. **AI agent** otomatik olarak:
        - Veri yapısını inceler
        - İstatistikleri hesaplar
        - Eksik değerleri bulur
        - Korelasyonları analiz eder
        - Aykırı değerleri tespit eder
        - Kapsamlı rapor oluşturur
    
    ### 🛠️ Teknik Özellikler
    
    - **Planning Pattern**: Agent önce plan yapar, sonra yürütür
    - **Stateful Execution**: Her adımın sonucu bir sonrakini etkiler
    - **LLM Integration**: Groq API ile Llama 3.1 70B modeli
    """)

# =============================================================================
# FOOTER
# =============================================================================

st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Data Insight Agent | Built with Streamlit & Groq"
    "</div>",
    unsafe_allow_html=True
)
