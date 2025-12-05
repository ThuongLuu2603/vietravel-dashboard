import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Vietravel Strategic Dashboard")

# CSS Style Vietravel
st.markdown("""
<style>
    .header-style {font-size: 22px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #ffcd00; background-color: #0051a3; padding: 8px 15px; border-radius: 5px;}
    .sub-header {font-size: 18px; font-weight: bold; color: #0051a3; border-bottom: 2px solid #ffcd00; margin-bottom: 10px;}
    .big-number {font-size: 36px; font-weight: bold; color: #2ca02c;}
    .metric-label {font-size: 16px; color: #555;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vietravel_Logo.png/1200px-Vietravel_Logo.png", width=200)
st.sidebar.header("BỘ LỌC DỮ LIỆU")
filter_period = st.sidebar.selectbox("Giai đoạn:", ["Tháng 11/2025", "Quý 4/2025", "Năm 2025"])
filter_hub = st.sidebar.multiselect("Đơn vị Kinh doanh (Hub):", ["Toàn Cty", "HO & ĐNB", "Miền Bắc", "Miền Trung", "Miền Tây"], default=["Toàn Cty", "HO & ĐNB"])

st.title(f"DASHBOARD CHIẾN LƯỢC VIETRAVEL - {filter_period}")

# ==============================================================================
# HÀNG 1: TOP LEFT & TOP RIGHT
# ==============================================================================
top_left, top_right = st.columns([1.8, 1.2])

with top_left:
    st.markdown('<div class="header-style">1. KINH DOANH: DOANH THU & HIỆU SUẤT</div>', unsafe_allow_html=True)
    
    # 1.1 Doanh thu & Lượt khách [Source: 19]
    st.markdown('<p class="sub-header">Doanh thu & Đóng góp của Hub (Tỷ VNĐ)</p>', unsafe_allow_html=True)
    months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'] # Demo 6 tháng cho gọn
    data_rev = {
        'Tháng': months * 4,
        'Hub': sorted(['HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây'] * 6),
        'Doanh Thu': [150, 160, 140, 180, 200, 210,  # HO
                      50, 55, 45, 60, 70, 80,        # Bắc
                      40, 42, 38, 50, 55, 60,        # Trung
                      20, 22, 18, 25, 30, 35]        # Tây
    }
    df_rev = pd.DataFrame(data_rev)
    # THÊM TEXT_AUTO=TRUE ĐỂ HIỆN SỐ TUYỆT ĐỐI
    fig_rev = px.bar(df_rev, x="Tháng", y="Doanh Thu", color="Hub", 
                     title="Doanh thu thực tế (Hiển thị số liệu)", text_auto=True,
                     color_discrete_sequence=['#0051a3', '#d62728', '#ffcd00', '#2ca02c'])
    fig_rev.update_traces(textposition='inside') # Số nằm trong cột
    st.plotly_chart(fig_rev, use_container_width=True)

    # 1.2 % Hoàn thành Kế hoạch [Source: 19]
    st.markdown('<p class="sub-header">Tỷ lệ Hoàn thành Kế hoạch (Bộ 3 Chỉ số)</p>', unsafe_allow_html=True)
    entities = ['Toàn Cty', 'HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
    act_rev_pct = [0.95, 1.05, 0.90, 0.85, 0.60]
    act_pax_pct = [0.98, 1.10, 0.95, 0.80, 0.50]
    act_gp_pct  = [0.88, 1.15, 0.65, 0.90, 0.40]

    fig_kpi = go.Figure()
    
    def add_kpi_group(name, values, color_solid, color_gap, offset_group):
        # HIỆN SỐ % TUYỆT ĐỐI TRÊN CỘT
        fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v, 1.0) for v in values],
                                 marker_color=color_solid, offsetgroup=offset_group, legendgroup=name,
                                 text=[f"{v*100:.0f}%" for v in values], textposition='auto')) # Hiện số %
        
        gaps = [max(1.0 - v, 0) for v in values]
        fig_kpi.add_trace(go.Bar(name=name+" Gap", x=entities, y=gaps,
                                 marker_color=color_gap, offsetgroup=offset_group, base=[min(v, 1.0) for v in values],
                                 legendgroup=name, showlegend=False, hoverinfo='skip'))
        
        overs = [max(v - 1.0, 0) for v in values]
        fig_kpi.add_trace(go.Bar(name=name+" Vượt", x=entities, y=overs,
                                 marker_color='#32CD32', offsetgroup=offset_group, base=1.0,
                                 legendgroup=name, showlegend=False, 
                                 text=[f"+{v*100:.0f}%" if v>0 else "" for v in overs], textposition='outside'))

    add_kpi_group("Doanh thu", act_rev_pct, '#1f77b4', '#aec7e8', 0)
    add_kpi_group("Lượt khách", act_pax_pct, '#ff7f0e', '#ffbb78', 1)
    add_kpi_group("Lãi gộp", act_gp_pct, '#9467bd', '#c5b0d5', 2)

    fig_kpi.update_layout(barmode='group', yaxis_tickformat='.0%', height=500,
                          title="Mức độ hoàn thành (Target = 100%)",
                          shapes=[dict(type="line", xref="paper", x0=0, x1=1, yref="y", y0=1, y1=1, line=dict(color="red", width=2, dash="dash"))])
    st.plotly_chart(fig_kpi, use_container_width=True)

with top_right:
    st.markdown('<div class="header-style">2. TÀI CHÍNH: LỢI NHUẬN & DÒNG TIỀN</div>', unsafe_allow_html=True)
    
    # 2.2 Big Number
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center;">
            <p class="metric-label">Biên Lợi Nhuận Ròng (Net Margin)</p>
            <p class="big-number">8.5% <span style="font-size: 20px; color: green;">▲ 0.5%</span></p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2.1 EBITDA [Source: 22]
    st.markdown('<p class="sub-header">EBITDA & Margin</p>', unsafe_allow_html=True)
    fig_ebitda = go.Figure()
    # HIỆN SỐ TRÊN CỘT VÀ ĐIỂM
    fig_ebitda.add_trace(go.Bar(name='EBITDA (Tỷ)', x=months, y=[25, 30, 20, 40, 45, 50], 
                                marker_color='#2ca02c', text=[25, 30, 20, 40, 45, 50], textposition='auto'))
    fig_ebitda.add_trace(go.Scatter(name='% Margin', x=months, y=[10, 12, 8, 15, 16, 18], yaxis='y2', 
                                    line=dict(color='orange', width=3), mode='lines+markers+text', text=[10, 12, 8, 15, 16, 18], textposition='top center'))
    fig_ebitda.update_layout(yaxis2=dict(overlaying='y', side='right', range=[0, 30]), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_ebitda, use_container_width=True)

    # 2.3 Waterfall [Source: 22]
    st.markdown('<p class="sub-header">Dòng tiền tự do (Cashflow)</p>', unsafe_allow_html=True)
    fig_waterfall = go.Figure(go.Waterfall(
        name="Cashflow", orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["Đầu kỳ", "Thu Tour", "Tiền mặt", "Trả NCC", "Chi phí", "Cuối kỳ"],
        y=[200, 800, 0, -400, -250, 0],
        text=[200, 800, 1000, -400, -250, 350], # HIỆN SỐ CỤ THỂ
        textposition="outside",
        connector={"line": {"color": "rgb(63, 63, 63)"}}
    ))
    st.plotly_chart(fig_waterfall, use_container_width=True)

# ==============================================================================
# HÀNG 2: THỊ TRƯỜNG & KHÁCH HÀNG
# ==============================================================================
st.markdown('<div class="header-style">3. THỊ TRƯỜNG & KHÁCH HÀNG</div>', unsafe_allow_html=True)
mid_1, mid_2, mid_3 = st.columns(3)

with mid_1:
    # 3.1 Cấu trúc thị trường [Source: 19]
    st.markdown('**Cấu trúc Doanh thu (Tỷ VNĐ)**')
    df_market = pd.DataFrame({
        "Năm": ["2023", "2023", "2023", "2024", "2024", "2024", "2025", "2025", "2025"],
        "Mảng": ["Inbound", "Outbound", "Domestic"] * 3,
        "Doanh Thu": [200, 500, 300, 250, 600, 350, 400, 800, 500] # Số liệu tuyệt đối
    })
    # TEXT_AUTO HIỆN SỐ TUYỆT ĐỐI
    fig_market = px.bar(df_market, x="Năm", y="Doanh Thu", color="Mảng", text_auto=True)
    st.plotly_chart(fig_market, use_container_width=True)

with mid_2:
    # 3.2 CLV vs CAC [Source: 19]
    st.markdown('**CLV vs CAC ($)**')
    fig_clv = go.Figure()
    # MODE='LINES+MARKERS+TEXT'
    fig_clv.add_trace(go.Scatter(name='CLV', x=['Q1', 'Q2', 'Q3', 'Q4'], y=[100, 120, 150, 180], 
                                 mode='lines+markers+text', text=[100, 120, 150, 180], textposition='top left'))
    fig_clv.add_trace(go.Scatter(name='CAC', x=['Q1', 'Q2', 'Q3', 'Q4'], y=[50, 55, 50, 45], 
                                 mode='lines+markers+text', text=[50, 55, 50, 45], textposition='bottom right', line=dict(dash='dot')))
    st.plotly_chart(fig_clv, use_container_width=True)

with mid_3:
    # 3.3 Thị phần tương đối [Source: 19]
    st.markdown('**Thị phần tương đối (%)**')
    df_bubble = pd.DataFrame({
        "Tuyến": ["Đông Bắc Á", "Âu Úc Mỹ", "Đông Nam Á", "Nội địa"],
        "Thị phần": [35, 20, 40, 25],
        "Tăng trưởng": [15, 10, 5, 8],
        "Doanh thu": [500, 800, 300, 400]
    })
    # TEXT='TUYẾN' ĐỂ HIỆN TÊN + SIZE BONG BÓNG
    fig_bubble = px.scatter(df_bubble, x="Thị phần", y="Tăng trưởng", size="Doanh thu", color="Tuyến",
                            text="Tuyến", size_max=60)
    fig_bubble.update_traces(textposition='top center')
    st.plotly_chart(fig_bubble, use_container_width=True)

mid_4, mid_5 = st.columns(2)
with mid_4:
    # 3.4 Tăng trưởng vs Ngành [Source: 19]
    st.markdown('**Tăng trưởng (%)**')
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(name='Vietravel', x=['Q1', 'Q2', 'Q3'], y=[15, 20, 25], text=[15, 20, 25], textposition='auto'))
    fig_growth.add_trace(go.Scatter(name='Ngành', x=['Q1', 'Q2', 'Q3'], y=[10, 12, 10], mode='lines+markers+text', text=[10, 12, 10], textposition='top center', line=dict(color='red')))
    st.plotly_chart(fig_growth, use_container_width=True)

with mid_5:
    # 3.5 ROI Marketing [Source: 22]
    st.markdown('**ROI Marketing (Tỷ VNĐ)**')
    df_mkt = pd.DataFrame({
        "Kênh": ["Facebook", "Google", "Tiktok", "Event", "Báo chí"],
        "Chi phí": [2, 5, 1, 3, 0.5],
        "Doanh thu": [20, 60, 15, 10, 2]
    })
    fig_mkt = px.scatter(df_mkt, x="Chi phí", y="Doanh thu", color="Kênh", size="Doanh thu", text="Kênh")
    fig_mkt.update_traces(textposition='top left')
    st.plotly_chart(fig_mkt, use_container_width=True)

# ==============================================================================
# HÀNG 3: NHÂN SỰ
# ==============================================================================
st.markdown('<div class="header-style">4. NHÂN SỰ & QUẢN TRỊ RỦI RO</div>', unsafe_allow_html=True)
bot_1, bot_2, bot_3 = st.columns(3)

with bot_1:
    # 4.1 Lợi nhuận/NS [Source: 25]
    st.markdown('**Năng suất (Triệu/Người)**')
    df_hr = pd.DataFrame({"Năm": [2023, 2024, 2025], "Vietravel": [200, 250, 300], "Ngành": [180, 200, 220]})
    fig_hr = px.line(df_hr, x="Năm", y=["Vietravel", "Ngành"], markers=True, text="Vietravel") # Hiện số của Vietravel
    fig_hr.update_traces(textposition="top left")
    st.plotly_chart(fig_hr, use_container_width=True)

with bot_2:
    st.markdown('**Giữ chân Key Person**')
    st.metric(label="Tỷ lệ giữ chân", value="95%", delta="-2%")
    st.table(pd.DataFrame({
        "Khu vực": ["Miền Bắc", "Miền Tây"],
        "Cảnh báo": ["GĐ Chi nhánh A", "TP Kinh doanh B"],
        "Rủi ro": ["Cao", "Trung bình"]
    }))

with bot_3:
    st.markdown('**Sẵn sàng kế thừa (%)**')
    z_data = [[100, 90, 20], [80, 50, 10], [100, 100, 80]]
    fig_heat = px.imshow(z_data, x=['TP', 'PGĐ', 'GĐ'], y=['Miền Tây', 'Miền Bắc', 'HO'],
                         color_continuous_scale='RdYlGn', text_auto=True) # Text_auto hiện số trong ô
    st.plotly_chart(fig_heat, use_container_width=True)
