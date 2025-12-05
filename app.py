import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Vietravel Executive Dashboard")

# CSS tùy chỉnh để làm đẹp giao diện (Style Vietravel)
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #0051a3;}
    .big-font {font-size: 24px !important; font-weight: bold; color: #0051a3;}
    .header-style {font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #ffcd00; background-color: #0051a3; padding: 5px 10px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.title("🚁 VIETRAVEL EXECUTIVE DASHBOARD - CHIẾN LƯỢC TOÀN CÔNG TY")
st.markdown("---")

# ==============================================================================
# PHẦN 1: MẢNG KINH DOANH (BUSINESS PERFORMANCE)
# ==============================================================================
st.markdown('<div class="header-style">1. KINH DOANH: HIỆU SUẤT & THỊ PHẦN</div>', unsafe_allow_html=True)

# --- 1.1 KEY METRICS (Số to đầu bảng) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Tổng Doanh Thu (YTD)", value="5,200 Tỷ", delta="12% vs YoY")
with col2:
    st.metric(label="Tổng Lượt Khách (Pax)", value="850,000", delta="8% vs YoY")
with col3:
    st.metric(label="Thị Phần Tương Đối (SoS)", value="1.5x", delta="Dẫn đầu")
with col4:
    st.metric(label="% Hoàn Thành KH Năm", value="92%", delta="Tiến độ tốt")

st.markdown("###") # Khoảng cách

# --- 1.2 BIỂU ĐỒ GROUPED STACKED BAR (Cái quan trọng nhất) ---
# Dữ liệu giả lập
hubs = ['Toàn Cty', 'HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
# % Thực đạt (Actual)
act_pax = [0.95, 1.05, 0.90, 0.60, 0.45]
act_rev = [0.92, 1.10, 0.95, 0.65, 0.50]
act_gp  = [0.88, 1.12, 0.60, 1.05, 0.30]

fig_trinity = go.Figure()

def add_stacked_group(fig, name, actuals, color_solid, color_gap, offset):
    # Phần thực đạt
    fig.add_trace(go.Bar(
        name=name, x=hubs, y=[min(x, 1.0) for x in actuals],
        marker_color=color_solid, offsetgroup=offset, legendgroup=name,
        text=[f"{x:.0%}" for x in actuals], textposition='auto'
    ))
    # Phần Gap (Thiếu)
    gaps = [max(1.0 - x, 0) for x in actuals]
    fig.add_trace(go.Bar(
        name=name + " (Gap)", x=hubs, y=gaps,
        marker_color=color_gap, offsetgroup=offset, base=[min(x, 1.0) for x in actuals],
        legendgroup=name, showlegend=False, hoverinfo="skip"
    ))
    # Phần Vượt (Over)
    over = [max(x - 1.0, 0) for x in actuals]
    fig.add_trace(go.Bar(
        name=name + " (Vượt)", x=hubs, y=over,
        marker_color='#32CD32', offsetgroup=offset, base=1.0,
        legendgroup=name, showlegend=False
    ))

# Thêm 3 nhóm cột
add_stacked_group(fig_trinity, "Khách (Pax)", act_pax, '#1f77b4', '#aec7e8', 0)
add_stacked_group(fig_trinity, "Doanh thu", act_rev, '#ff7f0e', '#ffbb78', 1)
add_stacked_group(fig_trinity, "Lãi gộp", act_gp, '#9467bd', '#c5b0d5', 2)

fig_trinity.update_layout(
    title_text="<b>BỘ 3 CHỈ SỐ HIỆU SUẤT (Performance Trinity)</b> - So sánh Thực tế vs Kế hoạch (100%)",
    yaxis_title="% Hoàn thành Kế hoạch",
    yaxis_tickformat=".0%",
    barmode='group',
    height=500,
    shapes=[dict(type="line", xref="paper", x0=0, x1=1, yref="y", y0=1, y1=1, line=dict(color="red", width=2, dash="dash"))]
)

st.plotly_chart(fig_trinity, use_container_width=True)


# --- 1.3 DOANH THU THEO THÁNG & CƠ CẤU (Bố cục chia đôi) ---
c1, c2 = st.columns(2)

with c1:
    # Standard Stacked Bar (Doanh thu theo tháng & Hub)
    df_rev = pd.DataFrame({
        "Tháng": ["T1", "T2", "T3", "T4", "T5", "T6"] * 4,
        "Hub": ["HO"]*6 + ["Bắc"]*6 + ["Trung"]*6 + ["Tây"]*6,
        "Doanh thu": np.random.randint(20, 100, 24)
    })
    fig_rev = px.bar(df_rev, x="Tháng", y="Doanh thu", color="Hub", title="<b>Xu hướng Doanh thu & Đóng góp của Hub</b>", text_auto=True)
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    # Combo Chart (Tăng trưởng so với ngành)
    months = ["T1", "T2", "T3", "T4", "T5", "T6"]
    y_vietravel = [15, 12, 20, 18, 22, 25]
    y_industry = [10, 8, 15, 12, 10, 12]
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(name='Vietravel Growth (%)', x=months, y=y_vietravel, marker_color='#0051a3'))
    fig_growth.add_trace(go.Scatter(name='Ngành Du lịch (%)', x=months, y=y_industry, mode='lines+markers', line=dict(color='red', width=3)))
    fig_growth.update_layout(title="<b>Tốc độ Tăng trưởng: Vietravel vs Ngành</b>")
    st.plotly_chart(fig_growth, use_container_width=True)

# ==============================================================================
# PHẦN 2: MẢNG TÀI CHÍNH (FINANCIAL HEALTH)
# ==============================================================================
st.markdown('<div class="header-style">2. TÀI CHÍNH: LỢI NHUẬN & DÒNG TIỀN</div>', unsafe_allow_html=True)

f1, f2 = st.columns(2)

with f1:
    # Waterfall Chart (Dòng tiền)
    fig_cash = go.Figure(go.Waterfall(
        name = "Cashflow", orientation = "v",
        measure = ["relative", "relative", "total", "relative", "relative", "total"],
        x = ["Đầu kỳ", "Thu Tour", "Tiền mặt sẵn có", "Chi trả NCC", "Chi phí HĐ", "Cuối kỳ"],
        textposition = "outside",
        text = ["+100", "+500", "600", "-300", "-150", "150"],
        y = [100, 500, 0, -300, -150, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    fig_cash.update_layout(title = "<b>Dòng tiền Tự do (Operating Cash Flow)</b>")
    st.plotly_chart(fig_cash, use_container_width=True)

with f2:
    # EBITDA Combo Chart
    fig_ebitda = go.Figure()
    fig_ebitda.add_trace(go.Bar(name='EBITDA (Tỷ)', x=months, y=[20, 25, 15, 30, 35, 40], marker_color='#2ca02c'))
    fig_ebitda.add_trace(go.Scatter(name='EBITDA Margin (%)', x=months, y=[5, 6, 4, 7, 8, 9], yaxis='y2', line=dict(color='orange')))
    fig_ebitda.update_layout(
        title="<b>Hiệu quả vận hành: EBITDA & Margin</b>",
        yaxis=dict(title="Giá trị (Tỷ VNĐ)"),
        yaxis2=dict(title="Margin (%)", overlaying='y', side='right')
    )
    st.plotly_chart(fig_ebitda, use_container_width=True)

# ==============================================================================
# PHẦN 3: MẢNG NHÂN SỰ (HUMAN CAPITAL)
# ==============================================================================
st.markdown('<div class="header-style">3. NHÂN SỰ: NĂNG SUẤT & KẾ THỪA</div>', unsafe_allow_html=True)

h1, h2 = st.columns([1, 2])

with h1:
    # Heatmap (Đội ngũ kế thừa)
    data_succession = [[100, 80, 0], [100, 50, 20], [100, 100, 100]]
    fig_heat = px.imshow(data_succession, 
                        labels=dict(x="Cấp bậc", y="Khu vực", color="% Sẵn sàng"),
                        x=['Trưởng phòng', 'Phó GĐ', 'Giám đốc'],
                        y=['Miền Tây', 'Miền Bắc', 'HO'],
                        color_continuous_scale='RdYlGn',
                        title="<b>Bản đồ nhiệt: Độ sẵn sàng đội ngũ kế thừa</b>")
    st.plotly_chart(fig_heat, use_container_width=True)

with h2:
    # Trend Line (Lợi nhuận/Nhân viên)
    df_prod = pd.DataFrame({
        "Năm": [2021, 2022, 2023, 2024, 2025],
        "Vietravel": [100, 150, 300, 450, 500],
        "TB Ngành": [100, 120, 200, 250, 300]
    })
    fig_prod = px.line(df_prod, x="Năm", y=["Vietravel", "TB Ngành"], markers=True, 
                      title="<b>Năng suất lao động: Lợi nhuận/Nhân sự (Triệu VNĐ)</b>")
    st.plotly_chart(fig_prod, use_container_width=True)
