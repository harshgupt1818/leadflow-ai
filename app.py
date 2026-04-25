import streamlit as st
from scraper import scrape_google_maps
from ai_processor import batch_process
from exporter import export_to_excel
import pandas as pd

st.set_page_config(page_title="LeadFlow AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');
* { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
.hero-section {
    background: linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0a1a2e 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 24px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,102,241,0.08) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(236,72,153,0.06) 0%, transparent 50%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #f472b6, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 16px;
    color: rgba(232,232,240,0.6);
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.5px;
}
.badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a78bfa;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 24px;
}
.metric-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(236,72,153,0.05));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
}
.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 40px;
    font-weight: 800;
    color: #a78bfa;
    display: block;
}
.metric-label {
    font-size: 12px;
    color: rgba(232,232,240,0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
div[data-testid="stTextInput"] label {
    color: rgba(232,232,240,0.8) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899) !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    padding: 16px 32px !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.3) !important;
}
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0 8px 24px rgba(16,185,129,0.3) !important;
}
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1, #ec4899) !important;
    border-radius: 4px !important;
}
hr { border-color: rgba(255,255,255,0.06) !important; }
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e8e8f0;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 13px;
    color: rgba(232,232,240,0.4);
    margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-section">
    <div class="badge">⚡ AI Powered</div>
    <h1 class="hero-title">LeadFlow AI</h1>
    <p class="hero-sub">Discover qualified business leads from Google Maps — AI-scored and ready to close</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🎯 Configure Your Search</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Enter the business type and location to find leads</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    business_type = st.text_input("🏢 Business Type", placeholder="e.g. digital agency, gym, restaurant")
with col2:
    city = st.text_input("📍 City", placeholder="e.g. Lucknow, Delhi, Mumbai")

max_leads = st.slider("📊 How many leads do you need?", min_value=10, max_value=100, value=10, step=10)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("⚡ Generate Leads Now", type="primary", use_container_width=True):
    if not business_type or not city:
        st.error("⚠️ Please fill in both Business Type and City!")
    else:
        query = business_type + " in " + city
        progress = st.progress(0)
        status = st.empty()

        status.info("🔍 Searching Google Maps for: " + query)
        progress.progress(25)
        leads = scrape_google_maps(query, max_leads)

        if not leads:
            st.error("❌ No leads found. Try a different query!")
        else:
            status.info("🤖 AI qualifying " + str(len(leads)) + " leads...")
            progress.progress(60)
            enriched_leads = batch_process(leads)

            status.info("📊 Generating Excel report...")
            progress.progress(85)

            filename = "leads_" + business_type + "_" + city + ".xlsx"
            filename = filename.replace(" ", "_")
            export_to_excel(enriched_leads, filename)
            progress.progress(100)
            status.success("✅ Done! " + str(len(enriched_leads)) + " leads are ready!")

            st.divider()
            df = pd.DataFrame(enriched_leads)

            st.markdown('<p class="section-title">📈 Results Overview</p>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown('<div class="metric-card"><span class="metric-num">' + str(len(df)) + '</span><span class="metric-label">Total Leads</span></div>', unsafe_allow_html=True)
            if 'status' in df.columns:
                hot = len(df[df['status']=='Hot'])
                warm = len(df[df['status']=='Warm'])
                cold = len(df[df['status']=='Cold'])
                with c2:
                    st.markdown('<div class="metric-card"><span class="metric-num" style="color:#f87171">' + str(hot) + '</span><span class="metric-label">🔥 Hot Leads</span></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown('<div class="metric-card"><span class="metric-num" style="color:#fbbf24">' + str(warm) + '</span><span class="metric-label">⚡ Warm Leads</span></div>', unsafe_allow_html=True)
                with c4:
                    st.markdown('<div class="metric-card"><span class="metric-num" style="color:#60a5fa">' + str(cold) + '</span><span class="metric-label">❄️ Cold Leads</span></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="section-title">📋 Lead Database</p>', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=400)

            st.markdown("<br>", unsafe_allow_html=True)
            with open(filename, "rb") as f:
                st.download_button(
                    label="📥 Download Excel Report",
                    data=f,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )