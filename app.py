import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Vietravel Strategic Dashboard")

# --- BẢNG MÀU CHIẾN LƯỢC ---
COLOR_MAP = {
    "Toàn Cty": "#333333", "HO & ĐNB": "#0051a3", "Miền Bắc": "#d62728", 
    "Miền Trung": "#ffcd00", "Miền Tây": "#2ca02c",
    "Inbound": "#17becf", "Outbound": "#0051a3", "Domestic": "#ff7f0e",
    "Đông Bắc Á": "#9467bd", "Âu Úc Mỹ": "#1f77b4", "Đông Nam Á": "#ff7f0e", "Nội địa": "#2ca02c",
    "Facebook": "#4267B2", "Google": "#DB4437", "Tiktok": "#000000", "Event": "#FFC107", "Báo chí": "#757575"
}

# --- CSS: TÙY CHỈNH GIAO DIỆN ---
st.markdown("""
<style>
    .metric-card {
        background-color: white; border-left: 5px solid #0051a3;
        padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-title {font-size: 14px; color: #555; font-weight: bold; text-transform: uppercase;}
    .metric-value {font-size: 32px; font-weight: 800; color: #0051a3;}
    .metric-delta {font-size: 16px; font-weight: bold; color: #2ca02c;}
    
    /* CSS CHO NET MARGIN (SỐ + CHART NẰM NGANG) */
    .net-margin-container {
        display: flex; align-items: center; justify-content: center; height: 100%;
    }
    .net-margin-val { font-size: 48px; font-weight: 900; color: #0051a3; }
    .net-margin-delta { font-size: 20px; color: #2ca02c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- HEADER & KEY METRICS ---
st.image("https://www.vietravel.com/Content/img/logo_en.png", width=200)
st.markdown("### 🚁 VIETRAVEL STRATEGIC COMMAND CENTER")

c1, c2, c3, c4, c5 = st.columns(5)
def metric_card(col, title, value, delta):
    col.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
    """, unsafe_allow_html=True)

metric_card(c1, "Doanh Thu", "520 Tỷ", "▲ 12%")
metric_card(c2, "Lượt Khách", "45.000", "▲ 8%")
metric_card(c3, "Biên Lợi Nhuận", "8.5%", "▲ 0.5%")
metric_card(c4, "Thị Phần RMS", "1.5x", "Dẫn đầu")
metric_card(c5, "Giữ Chân NS", "95%", "▼ 2%")

st.markdown("---")

# --- TAB VIEW ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 1. KINH DOANH", "🌍 2. THỊ TRƯỜNG", "💰 3. TÀI CHÍNH", "👥 4. NHÂN SỰ"])

# ==============================================================================
# TAB 1: KINH DOANH
# ==============================================================================
with tab1:
    col_b1, col_b2 = st.columns([1.5, 1])
    with col_b1:
        st.subheader("KPI: Tỷ lệ Hoàn thành Kế hoạch")
        # KPI Chart
        entities = ['Toàn Cty', 'HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
        fig_kpi = go.Figure()
        def add_kpi(name, vals, color, offset):
            fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v,1) for v in vals], marker_color=color, offsetgroup=offset, text=[f"{v:.0%}" for v in vals], textposition='auto'))
            fig_kpi.add_trace(go.Bar(name=name+" Gap", x=entities, y=[max(1-v,0) for v in vals], marker_color='#eee', offsetgroup=offset, base=[min(v,1) for v in vals], showlegend=False))
            fig_kpi.add_trace(go.Bar(name=name+" Over", x=entities, y=[max(v-1,0) for v in vals], marker_color='#32CD32', offsetgroup=offset, base=1.0, showlegend=False))
        add_kpi("Rev", [0.95, 1.05, 0.90, 0.85, 0.60], '#0051a3', 0)
        add_kpi("Pax", [0.98, 1.10, 0.95, 0.80, 0.50], '#ff7f0e', 1)
        add_kpi("GP",  [0.88, 1.15, 0.65, 0.90, 0.40], '#d62728', 2)
        fig_kpi.update_layout(barmode='group', height=400, shapes=[dict(type="line", xref="paper", x0=0, x1=1, yref="y", y0=1, y1=1, line=dict(color="red", width=2, dash="dash"))])
        st.plotly_chart(fig_kpi, use_container_width=True)
    
    with col_b2:
        st.subheader("Doanh thu thực tế (Tỷ VNĐ)")
        df_rev = pd.DataFrame({'Tháng': ['T1','T2','T3']*4, 'Hub': sorted(['HO','Bắc','Trung','Tây']*3), 'Rev': [150,160,170, 50,55,60, 40,42,45, 20,22,25]})
        fig_rev = px.bar(df_rev, x="Tháng", y="Rev", color="Hub", text_auto=True, color_discrete_map=COLOR_MAP)
        fig_rev.update_layout(height=400)
        st.plotly_chart(fig_rev, use_container_width=True)

# ==============================================================================
# TAB 2: THỊ TRƯỜNG
# ==============================================================================
with tab2:
    col_m1, col_m2 = st.columns([1.5, 1])
    with col_m1:
        st.subheader("Thị phần RMS (Theo Lượt Khách)")
        # RMS Bubble
        df_rms = pd.DataFrame({"Tuyến": ["Đ.Bắc Á", "Âu Úc", "ĐNA", "Nội địa"], "RMS": [0.8, 1.2, 1.5, 0.9], "Gr": [15,10,5,8], "Pax": [15000, 8000, 25000, 40000]})
        fig_bub = px.scatter(df_rms, x="RMS", y="Gr", size="Pax", color="Tuyến", text="Tuyến", size_max=60, color_discrete_map=COLOR_MAP)
        fig_bub.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="Đối thủ = Ta")
        fig_bub.update_layout(height=450, xaxis_title="RMS Index", yaxis_title="Tăng trưởng (%)")
        st.plotly_chart(fig_bub, use_container_width=True)
    
    with col_m2:
        st.subheader("Tăng trưởng vs Ngành")
        fig_gr = go.Figure()
        fig_gr.add_trace(go.Bar(name='Vietravel', x=['Q1','Q2','Q3'], y=[15,20,25], marker_color='#0051a3', text_auto=True))
        fig_gr.add_trace(go.Scatter(name='Ngành', x=['Q1','Q2','Q3'], y=[10,12,10], line=dict(color='red')))
        fig_gr.update_layout(height=450)
        st.plotly_chart(fig_gr, use_container_width=True)

# ==============================================================================
# TAB 3: TÀI CHÍNH (ĐÃ SỬA LỖI LAYOUT NET MARGIN)
# ==============================================================================
with tab3:
    st.subheader("Sức khỏe Tài chính")
    
    # --- ĐÂY LÀ CHỖ ĐIỀU CHỈNH THEO Ý BẠN ---
    # Layout ngang: [Số Liệu] - [Biểu đồ Line 6 tháng]
    
    with st.container():
        st.markdown("**Biên Lợi Nhuận Ròng (Net Margin)**")
        col_nm_1, col_nm_2 = st.columns([1, 3]) # Chia tỷ lệ 1:3
        
        with col_nm_1:
            # Hiển thị số to
            st.markdown("""
            <div class="net-margin-container">
                <div>
                    <div class="net-margin-val">8.5%</div>
                    <div class="net-margin-delta">▲ 0.5%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_nm_2:
            # Biểu đồ Sparkline nằm bên phải
            spark_x = ['T6','T7','T8','T9','T10','T11']
            spark_y = [5.0, 6.0, 5.5, 7.0, 8.0, 8.5]
            fig_sp = go.Figure(go.Scatter(x=spark_x, y=spark_y, mode='lines+markers+text', 
                                          text=[f"{v}%" for v in spark_y], textposition='top center', 
                                          line=dict(color='#2ca02c', width=4), 
                                          marker=dict(size=10, color='white', line=dict(width=2, color='green'))))
            fig_sp.update_layout(height=180, margin=dict(t=20,b=20,l=20,r=20), 
                                 xaxis=dict(showgrid=False), yaxis=dict(visible=False, range=[4,10]),
                                 title="Xu hướng 6 tháng gần nhất")
            st.plotly_chart(fig_sp, use_container_width=True)
            
    st.divider() # Đường kẻ phân cách
    
    # Các biểu đồ tài chính khác
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.subheader("EBITDA & Margin")
        fig_eb = go.Figure()
        fig_eb.add_trace(go.Bar(x=['T6','T7','T8','T9','T10','T11'], y=[25,30,20,40,45,50], name='EBITDA', marker_color='#2ca02c', text_auto=True))
        fig_eb.add_trace(go.Scatter(x=['T6','T7','T8','T9','T10','T11'], y=[10,12,8,15,16,18], name='Margin %', yaxis='y2', line=dict(color='orange', width=3)))
        fig_eb.update_layout(height=350, yaxis2=dict(overlaying='y', side='right'), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_eb, use_container_width=True)
        
    with c_f2:
        st.subheader("Dòng tiền (Waterfall)")
        fig_wf = go.Figure(go.Waterfall(orientation="v", measure=["relative","relative","total","relative","relative","total"], 
                                        x=["Đầu kỳ","Thu","Tiền mặt","Trả NCC","Chi phí","Cuối kỳ"], 
                                        y=[200,800,0,-400,-250,0], text=[200,800,1000,-400,-250,350], connector={"line":{"color":"gray"}}))
        fig_wf.update_layout(height=350)
        st.plotly_chart(fig_wf, use_container_width=True)

# ==============================================================================
# TAB 4: NHÂN SỰ
# ==============================================================================
with tab4:
    c_h1, c_h2 = st.columns(2)
    with c_h1:
        st.subheader("ROI Marketing")
        df_mkt = pd.DataFrame({"Kênh": ["FB", "Google", "Event"], "Cost": [2, 5, 3], "Rev": [20, 60, 10]})
        fig_mkt = px.scatter(df_mkt, x="Cost", y="Rev", color="Kênh", size="Rev", text="Kênh", color_discrete_map=COLOR_MAP)
        fig_mkt.update_layout(height=400)
        st.plotly_chart(fig_mkt, use_container_width=True)
    
    with c_h2:
        st.subheader("Năng suất Nhân sự")
        df_hr = pd.DataFrame({"Năm":['2023','2024','2025']*2, "Hub":['Toàn Cty']*3+['HO']*3, "Prod":[180,200,220, 200,230,250]})
        fig_hr = px.bar(df_hr, x="Năm", y="Prod", color="Hub", barmode='group', text_auto=True, color_discrete_map=COLOR_MAP)
        fig_hr.update_layout(height=400)
        st.plotly_chart(fig_hr, use_container_width=True)
