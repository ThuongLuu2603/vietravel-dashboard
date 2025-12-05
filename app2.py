import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Vietravel Executive Dashboard")

# --- BẢNG MÀU CHIẾN LƯỢC ---
COLOR_MAP = {
    "Toàn Cty": "#333333", "HO & ĐNB": "#0051a3", "Miền Bắc": "#d62728", 
    "Miền Trung": "#ffcd00", "Miền Tây": "#2ca02c",
    "Inbound": "#17becf", "Outbound": "#0051a3", "Domestic": "#ff7f0e",
    "Đông Bắc Á": "#9467bd", "Âu Úc Mỹ": "#1f77b4", "Đông Nam Á": "#ff7f0e", "Nội địa": "#2ca02c",
    "Facebook": "#4267B2", "Google": "#DB4437", "Tiktok": "#000000", "Event": "#FFC107", "Báo chí": "#757575"
}

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    /* Metric Card đẹp */
    .metric-card {
        background-color: white; border-left: 5px solid #0051a3;
        padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-title {font-size: 14px; color: #555; font-weight: bold; text-transform: uppercase;}
    .metric-value {font-size: 32px; font-weight: 800; color: #0051a3;}
    .metric-delta {font-size: 16px; font-weight: bold; color: #2ca02c;}
    
    /* Tab Font size */
    button[data-baseweb="tab"] {font-size: 18px !important; font-weight: bold !important;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vietravel_Logo.png/1200px-Vietravel_Logo.png", width=200)
    st.header("BỘ LỌC")
    st.selectbox("Giai đoạn", ["Tháng 11/2025", "Quý 4/2025", "Năm 2025"])
    st.multiselect("Hub", ["Toàn Cty", "HO", "Miền Bắc", "Miền Trung", "Miền Tây"], default=["Toàn Cty"])

# --- HEADER & KEY METRICS (LUÔN HIỂN THỊ) ---
st.markdown("### 🚁 VIETRAVEL STRATEGIC COMMAND CENTER")

# Hàng chỉ số quan trọng nhất (Big Numbers)
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

# --- PHÂN TAB NỘI DUNG (GIẢI QUYẾT VẤN ĐỀ RỐI MẮT) ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 1. HIỆU SUẤT KINH DOANH", "🌍 2. THỊ TRƯỜNG & KHÁCH HÀNG", "💰 3. TÀI CHÍNH", "👥 4. NHÂN SỰ & MKT"])

# ==============================================================================
# TAB 1: KINH DOANH (TRỌNG TÂM KPI)
# ==============================================================================
with tab1:
    col_biz_1, col_biz_2 = st.columns([2, 1])
    
    with col_biz_1:
        st.subheader("Tỷ lệ Hoàn thành Kế hoạch (Target = 100%)")
        # BIỂU ĐỒ GROUPED STACKED BAR (QUAN TRỌNG NHẤT)
        entities = ['Toàn Cty', 'HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
        fig_kpi = go.Figure()
        def add_kpi(name, vals, color, offset):
            fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v,1) for v in vals], marker_color=color, offsetgroup=offset, text=[f"{v:.0%}" for v in vals], textposition='auto'))
            fig_kpi.add_trace(go.Bar(name=name+" Gap", x=entities, y=[max(1-v,0) for v in vals], marker_color='#eee', offsetgroup=offset, base=[min(v,1) for v in vals], showlegend=False))
            fig_kpi.add_trace(go.Bar(name=name+" Vượt", x=entities, y=[max(v-1,0) for v in vals], marker_color='#32CD32', offsetgroup=offset, base=1.0, showlegend=False))

        add_kpi("Doanh thu", [0.95, 1.05, 0.90, 0.85, 0.60], '#0051a3', 0)
        add_kpi("Lượt khách", [0.98, 1.10, 0.95, 0.80, 0.50], '#ff7f0e', 1)
        add_kpi("Lãi gộp", [0.88, 1.15, 0.65, 0.90, 0.40], '#d62728', 2)
        
        fig_kpi.update_layout(barmode='group', height=450, yaxis_tickformat='.0%', 
                             legend=dict(orientation="h", y=1.1),
                             shapes=[dict(type="line", xref="paper", x0=0, x1=1, yref="y", y0=1, y1=1, line=dict(color="red", width=2, dash="dash"))])
        st.plotly_chart(fig_kpi, use_container_width=True)

    with col_biz_2:
        st.subheader("Doanh thu thực tế (Tỷ VNĐ)")
        # BIỂU ĐỒ STANDARD STACKED BAR
        df_rev = pd.DataFrame({'Tháng': ['T1','T2','T3']*4, 'Hub': sorted(['HO','Bắc','Trung','Tây']*3), 'Rev': [150,160,170, 50,55,60, 40,42,45, 20,22,25]})
        fig_rev = px.bar(df_rev, x="Tháng", y="Rev", color="Hub", text_auto=True, color_discrete_map=COLOR_MAP)
        fig_rev.update_layout(height=450, legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_rev, use_container_width=True)

# ==============================================================================
# TAB 2: THỊ TRƯỜNG (RMS & CẤU TRÚC)
# ==============================================================================
with tab2:
    col_mkt_1, col_mkt_2 = st.columns([1.5, 1])
    
    with col_mkt_1:
        st.subheader("Thị phần Tương đối RMS (Theo Lượt Khách)")
        st.caption("Trục hoành: Chỉ số RMS (>1 là Dẫn đầu). Bóng to = Đông khách.")
        # BIỂU ĐỒ BUBBLE (PAX & MÀU THEO TUYẾN)
        df_rms = pd.DataFrame({
            "Tuyến": ["Đông Bắc Á", "Âu Úc Mỹ", "Đông Nam Á", "Nội địa"],
            "RMS": [0.8, 1.2, 1.5, 0.9],
            "Growth": [15, 10, 5, 8],
            "Pax": [15000, 8000, 25000, 40000]
        })
        df_rms["Vị thế"] = df_rms["RMS"].apply(lambda x: "Dẫn đầu" if x>1 else "Theo sau")
        
        fig_bub = px.scatter(df_rms, x="RMS", y="Growth", size="Pax", color="Tuyến", 
                             text="Tuyến", size_max=70, color_discrete_map=COLOR_MAP)
        fig_bub.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="Đối thủ = Ta")
        fig_bub.update_traces(textposition='top center')
        fig_bub.update_layout(height=500, xaxis_title="Chỉ số RMS", yaxis_title="Tăng trưởng (%)")
        st.plotly_chart(fig_bub, use_container_width=True)

    with col_mkt_2:
        # Cấu trúc doanh thu
        st.subheader("Cấu trúc Doanh thu")
        df_str = pd.DataFrame({"Năm":['2023','2024','2025']*3, "Mảng":['Inbound']*3+['Outbound']*3+['Domestic']*3, "Rev":[200,250,300, 500,600,700, 300,350,400]})
        fig_str = px.bar(df_str, x="Năm", y="Rev", color="Mảng", text_auto=True, color_discrete_map=COLOR_MAP)
        fig_str.update_layout(height=230, margin=dict(b=0))
        st.plotly_chart(fig_str, use_container_width=True)
        
        # Growth vs Industry
        st.subheader("Tăng trưởng vs Ngành")
        fig_gr = go.Figure()
        fig_gr.add_trace(go.Bar(name='Vietravel', x=['Q1','Q2','Q3'], y=[15,20,25], marker_color='#0051a3', text_auto=True))
        fig_gr.add_trace(go.Scatter(name='Ngành', x=['Q1','Q2','Q3'], y=[10,12,10], line=dict(color='red')))
        fig_gr.update_layout(height=230, margin=dict(t=30))
        st.plotly_chart(fig_gr, use_container_width=True)

    # CLV vs CAC (Full width dưới cùng tab này)
    st.subheader("Hiệu quả Khách hàng: CLV vs CAC")
    fig_clv = go.Figure()
    fig_clv.add_trace(go.Scatter(x=['Q1','Q2','Q3','Q4'], y=[100,120,150,180], name='CLV (Giá trị)', line=dict(color='#0051a3', width=3), mode='lines+markers+text', textposition='top left'))
    fig_clv.add_trace(go.Scatter(x=['Q1','Q2','Q3','Q4'], y=[50,55,50,45], name='CAC (Chi phí)', line=dict(color='#d62728', dash='dot'), mode='lines+markers+text', textposition='bottom right'))
    fig_clv.update_layout(height=300)
    st.plotly_chart(fig_clv, use_container_width=True)


# ==============================================================================
# TAB 3: TÀI CHÍNH
# ==============================================================================
with tab3:
    col_fin_1, col_fin_2 = st.columns(2)
    
    with col_fin_1:
        st.subheader("Xu hướng Net Margin (6 Tháng)")
        # Sparkline to, rõ
        spark_x = ['T6','T7','T8','T9','T10','T11']
        spark_y = [5.0, 6.0, 5.5, 7.0, 8.0, 8.5]
        fig_sp = go.Figure(go.Scatter(x=spark_x, y=spark_y, mode='lines+markers+text', text=[f"{v}%" for v in spark_y], textposition='top center', line=dict(color='#2ca02c', width=3), marker=dict(size=10, color='white', line=dict(width=2, color='green'))))
        fig_sp.update_layout(height=300, xaxis=dict(showgrid=False), yaxis=dict(visible=False, range=[4,10]))
        st.plotly_chart(fig_sp, use_container_width=True)
        
    with col_fin_2:
        st.subheader("EBITDA & Margin")
        fig_eb = go.Figure()
        fig_eb.add_trace(go.Bar(x=['T6','T7','T8','T9','T10','T11'], y=[25,30,20,40,45,50], name='EBITDA', marker_color='#2ca02c', text_auto=True))
        fig_eb.add_trace(go.Scatter(x=['T6','T7','T8','T9','T10','T11'], y=[10,12,8,15,16,18], name='Margin %', yaxis='y2', line=dict(color='orange', width=3)))
        fig_eb.update_layout(height=300, yaxis2=dict(overlaying='y', side='right'), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_eb, use_container_width=True)

    st.subheader("Dòng tiền Tự do (Waterfall)")
    fig_wf = go.Figure(go.Waterfall(orientation="v", measure=["relative","relative","total","relative","relative","total"], x=["Đầu kỳ","Thu","Tiền mặt","Trả NCC","Chi phí","Cuối kỳ"], y=[200,800,0,-400,-250,0], text=[200,800,1000,-400,-250,350], connector={"line":{"color":"gray"}}))
    fig_wf.update_layout(height=400)
    st.plotly_chart(fig_wf, use_container_width=True)

# ==============================================================================
# TAB 4: NHÂN SỰ & HỖ TRỢ
# ==============================================================================
with tab4:
    col_hr_1, col_hr_2 = st.columns(2)
    
    with col_hr_1:
        st.subheader("ROI Marketing (Tỷ VNĐ)")
        df_mkt = pd.DataFrame({"Kênh": ["Facebook", "Google", "Tiktok", "Event", "Báo chí"], "Cost": [2, 5, 1, 3, 0.5], "Rev": [20, 60, 15, 10, 2]})
        fig_mkt = px.scatter(df_mkt, x="Cost", y="Rev", color="Kênh", size="Rev", text="Kênh", color_discrete_map=COLOR_MAP)
        fig_mkt.update_traces(textposition='top left')
        fig_mkt.update_layout(height=400)
        st.plotly_chart(fig_mkt, use_container_width=True)

    with col_hr_2:
        st.subheader("Năng suất Nhân sự (Triệu/Người)")
        # Grouped Bar cho NS như yêu cầu
        df_hr = pd.DataFrame({"Năm":['2023','2024','2025']*5, "Đơn vị":sorted(['Toàn Cty','HO','Bắc','Trung','Tây']*3), "Prod":[180,200,220, 200,230,250, 150,170,190, 160,180,200, 120,130,140]})
        fig_hr = px.bar(df_hr, x="Năm", y="Prod", color="Đơn vị", barmode='group', text_auto=True, color_discrete_map=COLOR_MAP)
        fig_hr.update_layout(height=400)
        st.plotly_chart(fig_hr, use_container_width=True)
        
    c_h1, c_h2 = st.columns(2)
    with c_h1:
        st.subheader("Rủi ro Nhân sự Key")
        st.table(pd.DataFrame({"Khu vực": ["Miền Bắc", "Miền Tây"], "Vị trí": ["GĐ Chi nhánh", "TP Kinh doanh"], "Rủi ro": ["Cao 🔴", "TB 🟡"]}))
    with c_h2:
        st.subheader("Độ sẵn sàng Kế thừa")
        fig_heat = px.imshow([[100, 90, 20], [80, 50, 10], [100, 100, 80]], x=['TP', 'PGĐ', 'GĐ'], y=['Tây', 'Bắc', 'HO'], color_continuous_scale='RdYlGn', text_auto=True)
        fig_heat.update_layout(height=300)
        st.plotly_chart(fig_heat, use_container_width=True)
