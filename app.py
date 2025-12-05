import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG (LAYOUT RỘNG TỐI ĐA) ---
st.set_page_config(layout="wide", page_title="Vietravel One-Row Dashboard", initial_sidebar_state="collapsed")

# --- BẢNG MÀU ---
COLOR_MAP = {
    "Toàn Cty": "#333333", "HO & ĐNB": "#0051a3", "Miền Bắc": "#d62728", 
    "Miền Trung": "#ffcd00", "Miền Tây": "#2ca02c",
    "Inbound": "#17becf", "Outbound": "#0051a3", "Domestic": "#ff7f0e",
    "Đông Bắc Á": "#9467bd", "Âu Úc Mỹ": "#1f77b4", "Đông Nam Á": "#ff7f0e", "Nội địa": "#2ca02c",
    "Facebook": "#4267B2", "Google": "#DB4437", "Tiktok": "#000000", "Event": "#FFC107", "Báo chí": "#757575"
}

# --- CSS: GIẢM PADDING, TỐI ƯU KHÔNG GIAN ---
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem; padding-left: 1rem; padding-right: 1rem;}
    .header-style {font-size: 18px; font-weight: bold; color: #fff; background-color: #0051a3; padding: 5px 10px; border-radius: 5px; margin-bottom: 10px;}
    .metric-card {
        background-color: #f8f9fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px; text-align: center;
    }
    .metric-val {font-size: 24px; font-weight: 800; color: #0051a3;}
    .metric-delta {font-size: 14px; font-weight: bold; color: #2ca02c;}
    .small-title {font-size: 14px; font-weight: bold; color: #555; text-align: center; margin-bottom: 5px;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
c_logo, c_title, c_sel = st.columns([1, 4, 1])
with c_logo:
    st.image("https://www.vietravel.com/Content/img/logo_en.png", width=150)
with c_title:
    st.markdown("<h2 style='text-align: center; color: #0051a3; margin:0;'>DASHBOARD CHIẾN LƯỢC (ONE-ROW VIEW)</h2>", unsafe_allow_html=True)
with c_sel:
    st.selectbox("", ["Tháng 11/2025", "Năm 2025"], label_visibility="collapsed")

st.markdown("---")

# --- HÀNG 1: KEY METRICS ---
m1, m2, m3, m4, m5 = st.columns(5)
def metric(col, label, val, delta):
    col.markdown(f"""
    <div class="metric-card">
        <div style="font-size:12px; font-weight:bold; color:#666;">{label}</div>
        <div class="metric-val">{val}</div>
        <div class="metric-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

metric(m1, "DOANH THU", "520 Tỷ", "▲ 12%")
metric(m2, "LƯỢT KHÁCH", "45.000", "▲ 8%")
metric(m3, "BIÊN LỢI NHUẬN", "8.5%", "▲ 0.5%")
metric(m4, "THỊ PHẦN RMS", "1.5x", "Dẫn đầu")
metric(m5, "GIỮ CHÂN NS", "95%", "▼ 2%")

# ==============================================================================
# KHU VỰC CHÍNH: CHIA 2 CỘT LỚN (KINH DOANH TRÁI - TÀI CHÍNH PHẢI)
# ==============================================================================
col_main_L, col_main_R = st.columns([1.8, 1.2])

# --- CỘT TRÁI: KINH DOANH (XẾP 1 HÀNG NGANG) ---
with col_main_L:
    st.markdown('<div class="header-style">1. KINH DOANH</div>', unsafe_allow_html=True)
    
    # CHIA LÀM 2 CỘT CON ĐỂ KPI VÀ DOANH THU NẰM NGANG
    bz1, bz2 = st.columns(2)
    
    with bz1:
        st.markdown('<div class="small-title">KPI (% Hoàn thành)</div>', unsafe_allow_html=True)
        # KPI Chart
        entities = ['Cty', 'HO', 'Bắc', 'Trung', 'Tây']
        fig_kpi = go.Figure()
        def add_kpi(name, vals, color, offset):
            fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v,1) for v in vals], marker_color=color, offsetgroup=offset, text=[f"{v:.0%}" for v in vals], textposition='auto'))
            fig_kpi.add_trace(go.Bar(name=name+"Gap", x=entities, y=[max(1-v,0) for v in vals], marker_color='#eee', offsetgroup=offset, base=[min(v,1) for v in vals], showlegend=False))
            fig_kpi.add_trace(go.Bar(name=name+"Over", x=entities, y=[max(v-1,0) for v in vals], marker_color='#32CD32', offsetgroup=offset, base=1.0, showlegend=False))
        add_kpi("Rev", [0.95, 1.05, 0.90, 0.85, 0.60], '#0051a3', 0)
        add_kpi("Pax", [0.98, 1.10, 0.95, 0.80, 0.50], '#ff7f0e', 1)
        add_kpi("GP",  [0.88, 1.15, 0.65, 0.90, 0.40], '#d62728', 2)
        fig_kpi.update_layout(barmode='group', height=250, margin=dict(t=10,b=0,l=0,r=0), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_kpi, use_container_width=True)

    with bz2:
        st.markdown('<div class="small-title">Doanh thu thực tế</div>', unsafe_allow_html=True)
        # Revenue Chart
        df_rev = pd.DataFrame({'T': ['T1','T2','T3']*4, 'Hub': sorted(['HO','Bắc','Trung','Tây']*3), 'Rev': [150,160,170, 50,55,60, 40,42,45, 20,22,25]})
        fig_rev = px.bar(df_rev, x="T", y="Rev", color="Hub", text_auto=True, color_discrete_map=COLOR_MAP)
        fig_rev.update_layout(height=250, margin=dict(t=10,b=0,l=0,r=0), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_rev, use_container_width=True)

# --- CỘT PHẢI: TÀI CHÍNH ---
with col_main_R:
    st.markdown('<div class="header-style">2. TÀI CHÍNH</div>', unsafe_allow_html=True)
    # Sparkline Net Margin
    spark_y = [5,6,5.5,7,8,8.5]
    fig_sp = go.Figure(go.Scatter(x=['T6','T7','T8','T9','T10','T11'], y=spark_y, mode='lines+markers+text', text=spark_y, textposition='top center', line=dict(color='#2ca02c')))
    fig_sp.update_layout(height=100, margin=dict(t=20,b=20,l=20,r=20), xaxis=dict(showgrid=False, visible=False), yaxis=dict(visible=False, range=[4,10]), title="Net Margin Trend", title_font_size=12)
    st.plotly_chart(fig_sp, use_container_width=True)
    
    # EBITDA (Nhỏ gọn)
    fig_eb = go.Figure()
    fig_eb.add_trace(go.Bar(x=['T9','T10','T11'], y=[40,45,50], marker_color='#2ca02c', name="EBITDA", text_auto=True))
    fig_eb.update_layout(height=130, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title="EBITDA (3 Tháng)", title_font_size=12)
    st.plotly_chart(fig_eb, use_container_width=True)

# ==============================================================================
# HÀNG 2: THỊ TRƯỜNG & PHÂN TÍCH (TẤT CẢ VỀ 1 HÀNG - 5 CỘT)
# ==============================================================================
st.markdown('<div class="header-style">3. THỊ TRƯỜNG & PHÂN TÍCH (5 TRỤ CỘT)</div>', unsafe_allow_html=True)

# ĐÂY LÀ CHỖ BẠN YÊU CẦU: 5 BIỂU ĐỒ TRÊN 1 HÀNG
c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns(5)

with c_m1:
    st.markdown('<div class="small-title">1. Cấu trúc DT</div>', unsafe_allow_html=True)
    df_str = pd.DataFrame({"Năm":['24','25']*3, "Mảng":['In','Out','Dom']*2, "Rev":[250,300, 400,450, 300,320]})
    fig_str = px.bar(df_str, x="Năm", y="Rev", color="Mảng", text_auto=True, color_discrete_map=COLOR_MAP)
    fig_str.update_layout(height=250, margin=dict(t=10,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_str, use_container_width=True)

with c_m2:
    st.markdown('<div class="small-title">2. CLV vs CAC</div>', unsafe_allow_html=True)
    fig_clv = go.Figure()
    fig_clv.add_trace(go.Scatter(x=['Q3','Q4'], y=[150,180], name='CLV', line=dict(color='#0051a3')))
    fig_clv.add_trace(go.Scatter(x=['Q3','Q4'], y=[50,45], name='CAC', line=dict(dash='dot', color='red')))
    fig_clv.update_layout(height=250, margin=dict(t=10,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_clv, use_container_width=True)

with c_m3:
    st.markdown('<div class="small-title">3. Tăng trưởng</div>', unsafe_allow_html=True)
    fig_gr = go.Figure()
    fig_gr.add_trace(go.Bar(name='Vietravel', x=['Q1','Q2','Q3'], y=[15,20,25], marker_color='#0051a3', text_auto=True))
    fig_gr.add_trace(go.Scatter(name='Ngành', x=['Q1','Q2','Q3'], y=[10,12,10], line=dict(color='red')))
    fig_gr.update_layout(height=250, margin=dict(t=10,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_gr, use_container_width=True)

with c_m4:
    # ROI MARKETING ĐÃ ĐƯA LÊN ĐÂY
    st.markdown('<div class="small-title">4. ROI MKT</div>', unsafe_allow_html=True)
    df_mkt = pd.DataFrame({"Kênh": ["FB", "GG", "Evt"], "Cost": [2, 5, 3], "Rev": [20, 60, 10]})
    fig_mkt = px.scatter(df_mkt, x="Cost", y="Rev", color="Kênh", size="Rev", text="Kênh", color_discrete_map=COLOR_MAP)
    fig_mkt.update_layout(height=250, margin=dict(t=10,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_mkt, use_container_width=True)

with c_m5:
    # RMS ĐÃ ĐƯA LÊN ĐÂY (DÙNG LƯỢT KHÁCH)
    st.markdown('<div class="small-title">5. RMS (Khách)</div>', unsafe_allow_html=True)
    df_rms = pd.DataFrame({"Tuyến": ["ĐBA", "Âu", "ĐNA", "Dom"], "RMS": [0.8, 1.2, 1.5, 0.9], "Gr": [15,10,5,8], "Pax": [15, 8, 25, 40]})
    fig_bub = px.scatter(df_rms, x="RMS", y="Gr", size="Pax", color="Tuyến", text="Tuyến", color_discrete_map=COLOR_MAP)
    fig_bub.add_vline(x=1, line_dash="dash", line_color="red")
    fig_bub.update_layout(height=250, margin=dict(t=10,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_bub, use_container_width=True)

# ==============================================================================
# HÀNG 4: NHÂN SỰ (CŨNG CHO VỀ 1 HÀNG 3 CỘT CHO ĐỒNG BỘ)
# ==============================================================================
st.markdown('<div class="header-style">4. NHÂN SỰ & QUẢN TRỊ</div>', unsafe_allow_html=True)
h1, h2, h3 = st.columns(3)

with h1:
    st.markdown('<div class="small-title">Năng suất (Tr.VNĐ/NS)</div>', unsafe_allow_html=True)
    df_hr = pd.DataFrame({"Năm":['24','25']*2, "Hub":['Cty']*2+['Bắc']*2, "Prod":[200,220, 150,170]})
    fig_hr = px.bar(df_hr, x="Năm", y="Prod", color="Hub", barmode='group', text_auto=True, color_discrete_map=COLOR_MAP)
    fig_hr.update_layout(height=200, margin=dict(t=10,b=0,l=0,r=0), showlegend=False)
    st.plotly_chart(fig_hr, use_container_width=True)

with h2:
    st.markdown('<div class="small-title">Giữ chân Key Person</div>', unsafe_allow_html=True)
    st.table(pd.DataFrame({"Vị trí": ["GĐ CN A", "TP KD B"], "Rủi ro": ["Cao 🔴", "TB 🟡"]}))

with h3:
    st.markdown('<div class="small-title">Kế thừa (%)</div>', unsafe_allow_html=True)
    z = [[90, 20], [100, 80]]
    fig_heat = px.imshow(z, x=['PGĐ', 'GĐ'], y=['Bắc', 'HO'], color_continuous_scale='RdYlGn', text_auto=True)
    fig_heat.update_layout(height=200, margin=dict(t=10,b=0,l=0,r=0))
    st.plotly_chart(fig_heat, use_container_width=True)
