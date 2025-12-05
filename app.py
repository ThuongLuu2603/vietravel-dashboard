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

# --- SIDEBAR FILTERS (Theo yêu cầu mục Bố cục) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vietravel_Logo.png/1200px-Vietravel_Logo.png", width=200) # Logo giả lập
st.sidebar.header("BỘ LỌC DỮ LIỆU")
filter_period = st.sidebar.selectbox("Giai đoạn:", ["Tháng 11/2025", "Quý 4/2025", "Năm 2025"])
filter_hub = st.sidebar.multiselect("Đơn vị Kinh doanh (Hub):", ["Toàn Cty", "HO & ĐNB", "Miền Bắc", "Miền Trung", "Miền Tây"], default=["Toàn Cty", "HO & ĐNB"])

st.title(f"DASHBOARD CHIẾN LƯỢC VIETRAVEL - {filter_period}")

# ==============================================================================
# HÀNG 1: TOP LEFT & TOP RIGHT (THEO BỐ CỤC CHỮ F)
# ==============================================================================

# Tạo 2 cột lớn: Trái (Kinh doanh) - Phải (Tài chính)
top_left, top_right = st.columns([1.8, 1.2])

with top_left:
    st.markdown('<div class="header-style">1. KINH DOANH: DOANH THU & HIỆU SUẤT</div>', unsafe_allow_html=True)
    
    # 1.1 Doanh thu & Lượt khách (Standard Stacked Bar)
    # [Source: 19] Trục hoành tháng, Trục tung tổng doanh thu, Lớp chồng là Hub
    st.markdown('<p class="sub-header">Doanh thu & Đóng góp của Hub (Tỷ VNĐ)</p>', unsafe_allow_html=True)
    months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
    hubs_list = ['HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
    data_rev = {
        'Tháng': months * 4,
        'Hub': sorted(hubs_list * 12),
        'Doanh Thu': np.random.randint(50, 200, 48) # Dữ liệu giả lập
    }
    df_rev = pd.DataFrame(data_rev)
    fig_rev = px.bar(df_rev, x="Tháng", y="Doanh Thu", color="Hub", 
                     title="Doanh thu thực tế theo Tháng (Standard Stacked Bar)",
                     color_discrete_sequence=['#0051a3', '#d62728', '#ffcd00', '#2ca02c']) # Xanh, Đỏ, Vàng, Lá
    st.plotly_chart(fig_rev, use_container_width=True)

    # 1.2 % Hoàn thành Kế hoạch (Grouped Stacked Bar - QUAN TRỌNG NHẤT)
    # [Source: 19] Trục tung %, 5 nhóm (Cty + 4 Hub), mỗi nhóm 3 cột (DT/Pax/Lãi)
    st.markdown('<p class="sub-header">Tỷ lệ Hoàn thành Kế hoạch (Bộ 3 Chỉ số)</p>', unsafe_allow_html=True)
    
    entities = ['Toàn Cty', 'HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
    # Dữ liệu % thực đạt (Actual)
    act_rev_pct = [0.95, 1.05, 0.90, 0.85, 0.60]
    act_pax_pct = [0.98, 1.10, 0.95, 0.80, 0.50]
    act_gp_pct  = [0.88, 1.15, 0.65, 0.90, 0.40]

    fig_kpi = go.Figure()
    
    def add_kpi_group(name, values, color_solid, color_gap, offset_group):
        # Vẽ phần thực đạt
        fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v, 1.0) for v in values],
                                 marker_color=color_solid, offsetgroup=offset_group, legendgroup=name,
                                 text=[f"{v:.0%}" for v in values], textposition='auto'))
        # Vẽ phần Gap (Thiếu)
        gaps = [max(1.0 - v, 0) for v in values]
        fig_kpi.add_trace(go.Bar(name=name+" Gap", x=entities, y=gaps,
                                 marker_color=color_gap, offsetgroup=offset_group, base=[min(v, 1.0) for v in values],
                                 legendgroup=name, showlegend=False, hoverinfo='skip'))
        # Vẽ phần Vượt
        overs = [max(v - 1.0, 0) for v in values]
        fig_kpi.add_trace(go.Bar(name=name+" Vượt", x=entities, y=overs,
                                 marker_color='#32CD32', offsetgroup=offset_group, base=1.0,
                                 legendgroup=name, showlegend=False))

    add_kpi_group("Doanh thu", act_rev_pct, '#1f77b4', '#aec7e8', 0)
    add_kpi_group("Lượt khách", act_pax_pct, '#ff7f0e', '#ffbb78', 1)
    add_kpi_group("Lãi gộp", act_gp_pct, '#9467bd', '#c5b0d5', 2)

    fig_kpi.update_layout(barmode='group', yaxis_tickformat='.0%', 
                          title="Mức độ hoàn thành mục tiêu (Target = 100%)",
                          shapes=[dict(type="line", xref="paper", x0=0, x1=1, yref="y", y0=1, y1=1, line=dict(color="red", width=2, dash="dash"))])
    st.plotly_chart(fig_kpi, use_container_width=True)

with top_right:
    st.markdown('<div class="header-style">2. TÀI CHÍNH: LỢI NHUẬN & DÒNG TIỀN</div>', unsafe_allow_html=True)
    
    # 2.2 Biên lợi nhuận ròng (Big Number + Sparkline) [Source: 22]
    # Mô phỏng hiển thị Big Number
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center;">
            <p class="metric-label">Biên Lợi Nhuận Ròng (Net Margin)</p>
            <p class="big-number">8.5% <span style="font-size: 20px; color: green;">▲ 0.5%</span></p>
        </div>
    """, unsafe_allow_html=True)
    # Vẽ Sparkline nhỏ bên dưới
    spark_data = [5, 6, 5.5, 7, 8, 8.5]
    fig_spark = px.line(x=list(range(6)), y=spark_data, height=100)
    fig_spark.update_xaxes(visible=False).update_yaxes(visible=False).update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_spark, use_container_width=True)

    # 2.1 EBITDA (Combo Chart) [Source: 22]
    st.markdown('<p class="sub-header">EBITDA & Margin</p>', unsafe_allow_html=True)
    fig_ebitda = go.Figure()
    fig_ebitda.add_trace(go.Bar(name='EBITDA (Tỷ)', x=months[:6], y=[25, 30, 20, 40, 45, 50], marker_color='#2ca02c'))
    fig_ebitda.add_trace(go.Scatter(name='% Margin', x=months[:6], y=[10, 12, 8, 15, 16, 18], yaxis='y2', line=dict(color='orange', width=3)))
    fig_ebitda.update_layout(yaxis2=dict(overlaying='y', side='right', range=[0, 30]), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_ebitda, use_container_width=True)

    # 2.3 Dòng tiền tự do (Waterfall) [Source: 22]
    st.markdown('<p class="sub-header">Dòng tiền tự do (Cashflow)</p>', unsafe_allow_html=True)
    fig_waterfall = go.Figure(go.Waterfall(
        name="Cashflow", orientation="v",
        measure=["relative", "relative", "total", "relative", "relative", "total"],
        x=["Đầu kỳ", "Thu Tour", "Tiền mặt", "Trả NCC", "Chi phí", "Cuối kỳ"],
        y=[200, 800, 0, -400, -250, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}}
    ))
    st.plotly_chart(fig_waterfall, use_container_width=True)

# ==============================================================================
# HÀNG 2: KHU VỰC GIỮA (THỊ TRƯỜNG & KHÁCH HÀNG) [Source: 19, 31]
# ==============================================================================
st.markdown('<div class="header-style">3. THỊ TRƯỜNG & KHÁCH HÀNG</div>', unsafe_allow_html=True)

mid_1, mid_2, mid_3 = st.columns(3)

with mid_1:
    # 3.1 Cấu trúc thị trường (100% Stacked Bar theo năm) [Source: 19]
    st.markdown('**Cấu trúc Doanh thu theo Năm**')
    df_market = pd.DataFrame({
        "Năm": ["2023", "2023", "2023", "2024", "2024", "2024", "2025", "2025", "2025"],
        "Mảng": ["Inbound", "Outbound", "Domestic"] * 3,
        "Tỷ trọng": [20, 50, 30, 25, 45, 30, 30, 40, 30]
    })
    fig_market = px.bar(df_market, x="Năm", y="Tỷ trọng", color="Mảng", title="", text_auto=True)
    st.plotly_chart(fig_market, use_container_width=True)

with mid_2:
    # 3.2 CLV vs CAC (Dual Line Chart) [Source: 19]
    st.markdown('**CLV (Giá trị KH) vs CAC (Chi phí sở hữu)**')
    fig_clv = go.Figure()
    fig_clv.add_trace(go.Scatter(name='CLV (Giá trị)', x=['Q1', 'Q2', 'Q3', 'Q4'], y=[10, 12, 15, 18], mode='lines+markers'))
    fig_clv.add_trace(go.Scatter(name='CAC (Chi phí)', x=['Q1', 'Q2', 'Q3', 'Q4'], y=[5, 5.5, 5, 4.5], mode='lines+markers', line=dict(dash='dot')))
    fig_clv.update_layout(title="Mục tiêu: Khoảng cách càng doãng ra càng tốt")
    st.plotly_chart(fig_clv, use_container_width=True)

with mid_3:
    # 3.3 Thị phần tương đối (Bubble Chart) [Source: 19]
    st.markdown('**Thị phần tương đối (Bubble Chart)**')
    # X: Thị phần, Y: Tăng trưởng, Size: Doanh thu
    df_bubble = pd.DataFrame({
        "Tuyến": ["Đông Bắc Á", "Âu Úc Mỹ", "Đông Nam Á", "Nội địa"],
        "Thị phần (%)": [35, 20, 40, 25],
        "Tăng trưởng (%)": [15, 10, 5, 8],
        "Doanh thu": [500, 800, 300, 400]
    })
    fig_bubble = px.scatter(df_bubble, x="Thị phần (%)", y="Tăng trưởng (%)", size="Doanh thu", color="Tuyến",
                            hover_name="Tuyến", size_max=60)
    st.plotly_chart(fig_bubble, use_container_width=True)

mid_4, mid_5 = st.columns(2)
with mid_4:
    # 3.4 Tăng trưởng so với ngành (Combo Chart) [Source: 19]
    st.markdown('**Tăng trưởng: Vietravel vs Ngành**')
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(name='Vietravel', x=['Q1', 'Q2', 'Q3'], y=[15, 20, 25]))
    fig_growth.add_trace(go.Scatter(name='Ngành', x=['Q1', 'Q2', 'Q3'], y=[10, 12, 10], line=dict(color='red')))
    st.plotly_chart(fig_growth, use_container_width=True)

with mid_5:
    # 3.5 Hiệu suất Marketing (Scatter Plot) [Source: 22]
    st.markdown('**Hiệu suất đầu tư Marketing (ROI)**')
    df_mkt = pd.DataFrame({
        "Kênh": ["Facebook", "Google", "Tiktok", "Event", "Báo chí"],
        "Chi phí (Tỷ)": [2, 5, 1, 3, 0.5],
        "Doanh thu (Tỷ)": [20, 60, 15, 10, 2]
    })
    fig_mkt = px.scatter(df_mkt, x="Chi phí (Tỷ)", y="Doanh thu (Tỷ)", color="Kênh", size="Doanh thu (Tỷ)", text="Kênh")
    st.plotly_chart(fig_mkt, use_container_width=True)


# ==============================================================================
# HÀNG 3: NHÂN SỰ & RỦI RO (BOTTOM) [Source: 25, 32]
# ==============================================================================
st.markdown('<div class="header-style">4. NHÂN SỰ & QUẢN TRỊ RỦI RO</div>', unsafe_allow_html=True)

bot_1, bot_2, bot_3 = st.columns(3)

with bot_1:
    # 4.1 Lợi nhuận/Nhân sự (Trend Line)
    st.markdown('**Năng suất: Lợi nhuận/Nhân viên**')
    df_hr = pd.DataFrame({"Năm": [2023, 2024, 2025], "Vietravel": [200, 250, 300], "Ngành": [180, 200, 220]})
    fig_hr = px.line(df_hr, x="Năm", y=["Vietravel", "Ngành"], markers=True)
    st.plotly_chart(fig_hr, use_container_width=True)

with bot_2:
    # 4.2 Giữ chân nhân sự Key (Scorecard)
    st.markdown('**Tỷ lệ giữ chân Key Person**')
    st.metric(label="Retention Rate (YTD)", value="95%", delta="-2% (Cảnh báo: Miền Bắc)")
    st.info("⚠️ Cảnh báo: 2 Giám đốc chi nhánh Miền Bắc đang có dấu hiệu rủi ro.")

with bot_3:
    # 4.3 Đội ngũ kế thừa (Heatmap)
    st.markdown('**Độ sẵn sàng kế thừa (Heatmap)**')
    z_data = [[100, 90, 20], [80, 50, 10], [100, 100, 80]] # Data mô phỏng
    fig_heat = px.imshow(z_data, x=['TP', 'PGĐ', 'GĐ'], y=['Miền Tây', 'Miền Bắc', 'HO'],
                         color_continuous_scale='RdYlGn', text_auto=True)
    st.plotly_chart(fig_heat, use_container_width=True)
