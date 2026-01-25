"""
app.py - Streamlit Ana Uygulaması
=================================
Görev: Team Lead (Mehmet)
Durum: TAMAMLANDI

Çalıştırma:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PAGE_TITLE, PAGE_ICON, PAGE_LAYOUT, PREVIEW_ROWS, validate_config
from agent.planner import Planner
from agent.executor import Executor
from memory.context import ExecutionContext

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)

if "context" not in st.session_state:
    st.session_state.context = None
if "plan" not in st.session_state:
    st.session_state.plan = None

st.title("📊 Data Insight Agent")
st.markdown("*AI destekli otomatik veri analizi*")

with st.sidebar:
    st.header("📁 Veri Kaynağı")
    data_source = st.radio("Kaynak seçin:", ["Dosya Yükle", "Örnek Veri"])
    df = None

    if data_source == "Dosya Yükle":
        uploaded_file = st.file_uploader("CSV dosyası yükleyin", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ {uploaded_file.name} yüklendi!")
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
    else:
        try:
            df = pd.read_csv("data/sample_data.csv")
            st.success("✅ sample_data.csv yüklendi!")
        except FileNotFoundError:
            st.error("❌ data/sample_data.csv bulunamadı!")

    st.divider()
    st.header("🔑 API Durumu")
    try:
        validate_config()
        st.success("✅ Groq API hazır")
    except ValueError as e:
        st.error(f"❌ {str(e)}")

if df is not None:
    st.subheader("📋 Veri Önizleme")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Satır", df.shape[0])
    with col2:
        st.metric("Sütun", df.shape[1])
    with col3:
        st.metric("Eksik", df.isnull().sum().sum())
    with col4:
        st.metric("MB", f"{df.memory_usage(deep=True).sum() / 1024 ** 2:.2f}")

    st.dataframe(df.head(PREVIEW_ROWS), use_container_width=True)
    st.divider()

    if st.button("🚀 Analizi Başlat", type="primary", use_container_width=True):
        try:
            context = ExecutionContext()
            context.set_dataframe(df)

            data_info = {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "missing": df.isnull().sum()[df.isnull().sum() > 0].to_dict()
            }

            st.subheader("📝 Analiz Planı")
            with st.spinner("Plan oluşturuluyor..."):
                planner = Planner()
                plan = planner.create_plan(data_info)

            for step in plan:
                st.write(f"**Adım {step['step_number']}:** {step['description']}")

            st.divider()
            st.subheader("⚙️ Yürütme")

            progress_bar = st.progress(0)
            status_text = st.empty()
            executor = Executor()

            for step_result in executor.execute_plan(plan, context):
                progress = step_result["step_number"] / step_result["total_steps"]
                progress_bar.progress(progress)
                status_text.text(f"İşleniyor: {step_result['description']}...")

                icon = "✅" if step_result["status"] == "success" else "❌"
                with st.expander(f"{icon} Adım {step_result['step_number']}: {step_result['description']}"):
                    if step_result["status"] == "success":
                        st.markdown(f"**Yorum:** {step_result['interpretation']}")
                    else:
                        st.error(f"Hata: {step_result['interpretation']}")

            status_text.text("✅ Analiz tamamlandı!")
            st.divider()

            st.subheader("📊 Final Rapor")
            from tools.reporter import generate_summary

            report_result = generate_summary(context)

            if report_result and report_result.get("success"):
                st.markdown(report_result.get("report_markdown", ""))
                st.download_button(
                    label="📥 Raporu İndir",
                    data=report_result.get("report_markdown", ""),
                    file_name="analiz_raporu.md",
                    mime="text/markdown"
                )

                findings = report_result.get("key_findings", [])
                if findings:
                    st.subheader("🔑 Önemli Bulgular")
                    for f in findings:
                        st.write(f"• {f}")
            else:
                st.warning("Rapor oluşturulamadı.")

        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
            st.exception(e)
else:
    st.info("👈 Sol taraftan veri yükleyin veya örnek veri seçin.")
    st.markdown("""
    ### 🎯 Bu Uygulama Ne Yapar?
    1. CSV dosyanızı yükleyin
    2. "Analizi Başlat" tıklayın
    3. AI agent otomatik analiz yapar

    ### 🛠️ Özellikler
    - Planning Pattern
    - Stateful Execution
    - LLM Integration (Groq)
    """)

st.divider()
st.markdown("<div style='text-align:center;color:gray;'>Data Insight Agent | Team Lead: Mehmet</div>",
            unsafe_allow_html=True)