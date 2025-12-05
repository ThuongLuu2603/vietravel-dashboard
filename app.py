import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Vietravel Strategic Dashboard")

# --- BẢNG MÀU CHIẾN LƯỢC ---
COLOR_MAP = {
    "Toàn Cty": "#333333",
    "HO & ĐNB": "#0051a3",    
    "Miền Bắc": "#d62728",    
    "Miền Trung": "#ffcd00",  
    "Miền Tây": "#2ca02c",    Aimport streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# --- CẤU HÌNH TRANG (ONE PAGE) ---
st.set_page_config(layout="wide", page_title="Vietravel One-Page View", initial_sidebar_state="collapsed")

# --- CSS TỐI ƯU KHÔNG GIAN ---
st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
    .metric-card {
        background-color: white; border: 1px solid #e0e0e0; border-radius: 5px; 
        padding: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .metric-title {font-size: 12px; color: #666; font-weight: bold; text-transform: uppercase;}
    .metric-val {font-size: 24px; font-weight: 800; color: #0051a3; line-height: 1.1;}
    .metric-delta {font-size: 12px; font-weight: bold; color: #2ca02c;}
    h3 {font-size: 16px !important; margin-bottom: 5px !important; padding-top: 0px !important; color: #0051a3;}
</style>
""", unsafe_allow_html=True)

# --- BẢNG MÀU ---
COLOR_MAP = {
    "Toàn Cty": "#333333", "HO & ĐNB": "#0051a3", "Miền Bắc": "#d62728", 
    "Miền Trung": "#ffcd00", "Miền Tây": "#2ca02c",
    "Inbound": "#17becf", "Outbound": "#0051a3", "Domestic": "#ff7f0e",
    "Đông Bắc Á": "#9467bd", "Âu Úc Mỹ": "#1f77b4", "Đông Nam Á": "#ff7f0e", "Nội địa": "#2ca02c",
    "Facebook": "#4267B2", "Google": "#DB4437", "Tiktok": "#000000", "Event": "#FFC107", "Báo chí": "#757575"
}

# --- HEADER ---
c_title, c_filter = st.columns([3, 1])
with c_title:
    st.markdown("### 🚁 VIETRAVEL STRATEGIC DASHBOARD (ONE-PAGE)")
with c_filter:
    period = st.selectbox("", ["Tháng 11/2025", "Quý 4/2025", "Năm 2025"], label_visibility="collapsed")

# --- HÀNG 1: KEY METRICS ---
def card(col, title, val, delta):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div><span class="metric-val">{val}</span> <span class="metric-delta">{delta}</span></div>
    </div>
    """, unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
card(m1, "Doanh Thu", "520 Tỷ", "▲ 12%")
card(m2, "Lượt Khách", "45.000", "▲ 8%")
card(m3, "Biên Lợi Nhuận", "8.5%", "▲ 0.5%")
card(m4, "Thị Phần (RMS)", "1.5x", "Dẫn đầu")
card(m5, "Giữ chân NS", "95%", "▼ 2%")

# --- HÀNG 2: CHIA LƯỚI 4 CỘT ---
col_biz, col_fin, col_mkt, col_hr = st.columns([1.2, 1, 1, 1])

# ================= CỘT 1: KINH DOANH =================
with col_biz:
    st.markdown("### 1. HIỆU SUẤT KINH DOANH")
    
    # 1. KPI Achievement
    entities = ['Cty', 'HO', 'Bắc', 'Trung', 'Tây']
    fig_kpi = go.Figure()
    def add_trace_kpi(name, vals, color, offset):
        fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v,1) for v in vals], marker_color=color, offsetgroup=offset, text=[f"{v:.0%}" for v in vals], textposition='auto'))
        fig_kpi.add_trace(go.Bar(name=name+"Gap", x=entities, y=[max(1-v,0) for v in vals], marker_color='#eee', offsetgroup=offset, base=[min(v,1) for v in vals], showlegend=False))
        fig_kpi.add_trace(go.Bar(name=name+"Over", x=entities, y=[max(v-1,0) for v in vals], marker_color='#32CD32', offsetgroup=offset, base=1.0, showlegend=False))

    add_trace_kpi("Rev", [0.95, 1.05, 0.90, 0.85, 0.60], '#0051a3', 0)
    add_trace_kpi("Pax", [0.98, 1.10, 0.95, 0.80, 0.50], '#ff7f0e', 1)
    add_trace_kpi("GP",  [0.88, 1.15, 0.65, 0.90, 0.40], '#d62728', 2)
    
    fig_kpi.update_layout(barmode='group', height=250, margin=dict(t=20,b=0,l=0,r=0), 
                          title_text="KPI: Rev | Pax | GP", title_font_size=12,
                          legend=dict(orientation="h", y=1.1, font=dict(size=10)))
    st.plotly_chart(fig_kpi, use_container_width=True)

    # 2. Revenue Trend
    df_rev = pd.DataFrame({'T': ['T1','T2','T3']*4, 'Hub': sorted(['HO','Bắc','Trung','Tây']*3), 'Rev': np.random.randint(20,100,12)})
    fig_rev = px.bar(df_rev, x="T", y="Rev", color="Hub", text_auto=True, color_discrete_map=COLOR_MAP)
    fig_rev.update_layout(height=180, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="Xu hướng Doanh thu", title_font_size=12)
    st.plotly_chart(fig_rev, use_container_width=True)

    # 3. Growth vs Industry (ĐÃ SỬA LỖI TẠI ĐÂY)
    fig_gr = go.Figure()
    # SỬA LỖI: Thay text_auto=True bằng text=[...]
    fig_gr.add_trace(go.Bar(name='Vietravel', x=['Q1','Q2','Q3'], y=[15,20,25], marker_color='#0051a3', text=[15,20,25], textposition='auto'))
    fig_gr.add_trace(go.Scatter(name='Ngành', x=['Q1','Q2','Q3'], y=[10,12,10], line=dict(color='red')))
    fig_gr.update_layout(height=150, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="Tăng trưởng vs Ngành", title_font_size=12)
    st.plotly_chart(fig_gr, use_container_width=True)


# ================= CỘT 2: TÀI CHÍNH =================
with col_fin:
    st.markdown("### 2. TÀI CHÍNH")
    
    # 1. Sparkline Net Margin
    spark_x = ['T6','T7','T8','T9','T10','T11']
    spark_y = [5,6,5.5,7,8,8.5]
    fig_sp = go.Figure(go.Scatter(x=spark_x, y=spark_y, mode='lines+markers+text', text=spark_y, textposition='top center', line=dict(color='#2ca02c')))
    fig_sp.update_layout(height=150, margin=dict(t=20,b=10,l=10,r=10), xaxis=dict(showgrid=False), yaxis=dict(visible=False, range=[4,10]), title_text="Net Margin (6 Tháng)", title_font_size=12)
    st.plotly_chart(fig_sp, use_container_width=True)

    # 2. EBITDA Combo
    fig_eb = go.Figure()
    # SỬA LỖI: Thêm text thủ công cho go.Bar
    fig_eb.add_trace(go.Bar(x=['T9','T10','T11'], y=[40,45,50], marker_color='#2ca02c', name="EBITDA", text=[40,45,50], textposition='auto'))
    fig_eb.add_trace(go.Scatter(x=['T9','T10','T11'], y=[15,16,18], yaxis='y2', line=dict(color='orange'), name="%"))
    fig_eb.update_layout(height=200, margin=dict(t=20,b=0,l=0,r=0), yaxis2=dict(overlaying='y', side='right'), showlegend=False, title_text="EBITDA & Margin", title_font_size=12)
    st.plotly_chart(fig_eb, use_container_width=True)

    # 3. Cashflow Waterfall
    fig_wf = go.Figure(go.Waterfall(orientation="v", measure=["relative", "total"], x=["Thu","Cuối kỳ"], y=[500, 300], connector={"line":{"color":"gray"}}))
    fig_wf.update_layout(height=200, margin=dict(t=20,b=0,l=0,r=0), title_text="Dòng tiền (Tóm tắt)", title_font_size=12)
    st.plotly_chart(fig_wf, use_container_width=True)

# ================= CỘT 3: THỊ TRƯỜNG =================
with col_mkt:
    st.markdown("### 3. THỊ TRƯỜNG")
    
    # 1. RMS Bubble (Lượt khách)
    df_rms = pd.DataFrame({
        "Tuyến": ["Đ.Bắc Á", "Âu Úc", "ĐNA", "Nội địa"], 
        "RMS": [0.8, 1.2, 1.5, 0.9], 
        "Gr": [15,10,5,8], 
        "Pax": [15, 8, 25, 40]
    })
    df_rms["Vị thế"] = df_rms["RMS"].apply(lambda x: "Dẫn đầu" if x>1 else "Theo sau")
    fig_bub = px.scatter(df_rms, x="RMS", y="Gr", size="Pax", color="Tuyến", text="Tuyến", color_discrete_map=COLOR_MAP)
    fig_bub.add_vline(x=1, line_dash="dash", line_color="red")
    fig_bub.update_layout(height=250, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="Thị phần RMS (Lượt khách)", title_font_size=12)
    st.plotly_chart(fig_bub, use_container_width=True)

    # 2. Market Structure
    df_struc = pd.DataFrame({"Năm":['24','25']*3, "Mảng":['Inbound']*2+['Outbound']*2+['Domestic']*2, "Rev":[250,300, 400,450, 300,320]})
    fig_str = px.bar(df_struc, x="Năm", y="Rev", color="Mảng", color_discrete_map=COLOR_MAP, text_auto=True)
    fig_str.update_layout(height=180, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="Cấu trúc Doanh thu", title_font_size=12)
    st.plotly_chart(fig_str, use_container_width=True)

    # 3. CLV vs CAC
    fig_clv = go.Figure()
    fig_clv.add_trace(go.Scatter(x=['Q3','Q4'], y=[150,180], name='CLV', line=dict(color='#0051a3')))
    fig_clv.add_trace(go.Scatter(x=['Q3','Q4'], y=[50,45], name='CAC', line=dict(dash='dot', color='red')))
    fig_clv.update_layout(height=150, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="CLV vs CAC", title_font_size=12)
    st.plotly_chart(fig_clv, use_container_width=True)

# ================= CỘT 4: MKT & NHÂN SỰ =================
with col_hr:
    st.markdown("### 4. HỖ TRỢ")

    # 1. ROI Marketing
    df_mkt = pd.DataFrame({"Kênh": ["FB", "Google", "Event"], "Cost": [2, 5, 3], "Rev": [20, 60, 10]})
    fig_mkt = px.scatter(df_mkt, x="Cost", y="Rev", color="Kênh", size="Rev", text="Kênh", color_discrete_map=COLOR_MAP)
    fig_mkt.update_layout(height=200, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="ROI Marketing", title_font_size=12)
    st.plotly_chart(fig_mkt, use_container_width=True)

    # 2. HR Productivity
    df_hr = pd.DataFrame({"Năm":['24','25']*2, "Hub":['Cty']*2+['Bắc']*2, "Prod":[200,220, 150,170]})
    fig_hr = px.bar(df_hr, x="Năm", y="Prod", color="Hub", barmode='group', text_auto=True, color_discrete_map=COLOR_MAP)
    fig_hr.update_layout(height=200, margin=dict(t=20,b=0,l=0,r=0), showlegend=False, title_text="Năng suất (Tr.VNĐ/NS)", title_font_size=12)
    st.plotly_chart(fig_hr, use_container_width=True)

    # 3. Succession Heatmap
    z = [[90, 20], [100, 80]]
    fig_heat = px.imshow(z, x=['PGĐ', 'GĐ'], y=['Bắc', 'HO'], color_continuous_scale='RdYlGn', text_auto=True)
    fig_heat.update_layout(height=180, margin=dict(t=20,b=0,l=0,r=0), title_text="Kế thừa (%)", title_font_size=12)
    st.plotly_chart(fig_heat, use_container_width=True)    "Inbound": "#17becf", "Outbound": "#0051a3", "Domestic": "#ff7f0e",
    # MÀU TUYẾN
    "Đông Bắc Á": "#9467bd", "Âu Úc Mỹ": "#1f77b4", "Đông Nam Á": "#ff7f0e", "Nội địa": "#2ca02c",
    # Kênh Marketing
    "Facebook": "#4267B2", "Google": "#DB4437", "Tiktok": "#000000", "Event": "#FFC107", "Báo chí": "#757575"
}

# CSS Style
st.markdown("""
<style>
    .header-style {font-size: 22px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #ffcd00; background-color: #0051a3; padding: 8px 15px; border-radius: 5px;}
    .metric-container {background-color: #ffffff; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e0e0e0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
    .metric-label {font-size: 14px; color: #888; font-weight: 600; text-transform: uppercase;}
    .metric-value {font-size: 36px; font-weight: 800; color: #0051a3;} 
    .metric-delta {font-size: 16px; font-weight: bold; color: #2ca02c;}
    
    /* CSS CHO NET MARGIN NGANG */
    .net-margin-box { display: flex; align-items: center; justify-content: center; height: 100%; }
    .nm-val { font-size: 40px; font-weight: 900; color: #0051a3; margin-right: 10px; }
    .nm-delta { font-size: 18px; font-weight: bold; color: #2ca02c; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://www.vietravel.com/Content/img/logo_en.png", width=200)
st.sidebar.header("BỘ LỌC DỮ LIỆU")
filter_period = st.sidebar.selectbox("Giai đoạn:", ["Tháng 11/2025", "Quý 4/2025", "Năm 2025"])

st.title(f"DASHBOARD CHIẾN LƯỢC VIETRAVEL - {filter_period}")

# ==============================================================================
# HÀNG 1: KINH DOANH & TÀI CHÍNH
# ==============================================================================
top_left, top_right = st.columns([1.8, 1.2])

# --- CỘT TRÁI: KINH DOANH ---
with top_left:
    st.markdown('<div class="header-style">1. KINH DOANH: DOANH THU & HIỆU SUẤT</div>', unsafe_allow_html=True)
    
    # 1.1 TỶ LỆ HOÀN THÀNH KẾ HOẠCH (Đã đưa lên trên)
    st.markdown('**Tỷ lệ Hoàn thành Kế hoạch (Target = 100%)**')
    entities = ['Toàn Cty', 'HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây']
    act_rev_pct = [0.95, 1.05, 0.90, 0.85, 0.60]
    act_pax_pct = [0.98, 1.10, 0.95, 0.80, 0.50]
    act_gp_pct  = [0.88, 1.15, 0.65, 0.90, 0.40]

    fig_kpi = go.Figure()
    def add_kpi_group(name, values, color_solid, color_gap, offset_group):
        fig_kpi.add_trace(go.Bar(name=name, x=entities, y=[min(v, 1.0) for v in values], marker_color=color_solid, offsetgroup=offset_group, text=[f"{v*100:.0f}%" for v in values], textposition='auto'))
        fig_kpi.add_trace(go.Bar(name=name+" Gap", x=entities, y=[max(1.0 - v, 0) for v in values], marker_color=color_gap, offsetgroup=offset_group, base=[min(v, 1.0) for v in values], showlegend=False))
        fig_kpi.add_trace(go.Bar(name=name+" Vượt", x=entities, y=[max(v - 1.0, 0) for v in values], marker_color='#32CD32', offsetgroup=offset_group, base=1.0, showlegend=False))

    add_kpi_group("Doanh thu", act_rev_pct, '#0051a3', '#aec7e8', 0)
    add_kpi_group("Lượt khách", act_pax_pct, '#ff7f0e', '#ffbb78', 1)
    add_kpi_group("Lãi gộp", act_gp_pct, '#d62728', '#f4cccc', 2)

    fig_kpi.update_layout(barmode='group', yaxis_tickformat='.0%', height=350, margin=dict(t=20, b=20), shapes=[dict(type="line", xref="paper", x0=0, x1=1, yref="y", y0=1, y1=1, line=dict(color="red", width=2, dash="dash"))])
    st.plotly_chart(fig_kpi, use_container_width=True)

    # 1.2 DOANH THU (Đã đưa xuống dưới)
    st.markdown('**Doanh thu & Đóng góp của Hub (Tỷ VNĐ)**')
    df_rev = pd.DataFrame({'Tháng': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'] * 4, 'Hub': sorted(['HO & ĐNB', 'Miền Bắc', 'Miền Trung', 'Miền Tây'] * 6), 'Doanh Thu': [150, 160, 140, 180, 200, 210, 50, 55, 45, 60, 70, 80, 40, 42, 38, 50, 55, 60, 20, 22, 18, 25, 30, 35]})
    fig_rev = px.bar(df_rev, x="Tháng", y="Doanh Thu", color="Hub", text_auto=True, color_discrete_map=COLOR_MAP)
    fig_rev.update_traces(textposition='inside', textfont_color='white') 
    st.plotly_chart(fig_rev, use_container_width=True)

# --- CỘT PHẢI: TÀI CHÍNH ---
with top_right:
    st.markdown('<div class="header-style">2. TÀI CHÍNH</div>', unsafe_allow_html=True)
    
    # --- 2.1 NET MARGIN (ĐÃ SỬA THÀNH 1 HÀNG NGANG) ---
    st.markdown("**Biên Lợi Nhuận Ròng (Net Margin)**")
    c_nm_val, c_nm_chart = st.columns([1, 2])
    
    with c_nm_val:
        st.markdown('<div class="net-margin-box"><span class="nm-val">8.5%</span><span class="nm-delta">▲ 0.5%</span></div>', unsafe_allow_html=True)
        
    with c_nm_chart:
        spark_y = [5.0, 6.0, 5.5, 7.0, 8.0, 8.5]
        fig_spark = go.Figure(go.Scatter(x=['T6','T7','T8','T9','T10','T11'], y=spark_y, mode='lines+markers+text', text=[f"{v}" for v in spark_y], textposition="top center", line=dict(color='#2ca02c', width=3)))
        fig_spark.update_layout(height=120, margin=dict(l=10, r=10, t=20, b=10), xaxis=dict(showgrid=False, showline=False), yaxis=dict(visible=False, range=[4, 10]))
        st.plotly_chart(fig_spark, use_container_width=True)
    
    # 2.2 EBITDA
    st.markdown('**EBITDA & Margin**')
    fig_ebitda = go.Figure()
    fig_ebitda.add_trace(go.Bar(name='EBITDA', x=['T1','T2','T3','T4','T5','T6'], y=[25, 30, 20, 40, 45, 50], marker_color='#2ca02c', text_auto=True))
    fig_ebitda.add_trace(go.Scatter(name='% Margin', x=['T1','T2','T3','T4','T5','T6'], y=[10, 12, 8, 15, 16, 18], yaxis='y2', line=dict(color='#ff7f0e', width=3)))
    fig_ebitda.update_layout(yaxis2=dict(overlaying='y', side='right'), legend=dict(orientation="h", y=1.1), margin=dict(t=30, b=0), height=300)
    st.plotly_chart(fig_ebitda, use_container_width=True)

    # 2.3 Waterfall
    st.markdown('**Dòng tiền (Cashflow)**')
    fig_wf = go.Figure(go.Waterfall(measure=["relative"]*5+["total"], x=["Đầu kỳ", "Thu", "Tiền", "Trả", "Chi", "Cuối"], y=[200, 800, 0, -400, -250, 0], text=[200, 800, 1000, -400, -250, 350], connector={"line": {"color": "gray"}}))
    fig_wf.update_layout(margin=dict(t=20, b=20), height=300)
    st.plotly_chart(fig_wf, use_container_width=True)

# ==============================================================================
# HÀNG 2: THỊ TRƯỜNG & KHÁCH HÀNG (GỘP TẤT CẢ VÀO 1 HÀNG 5 CỘT)
# ==============================================================================
st.markdown('<div class="header-style">3. THỊ TRƯỜNG & KHÁCH HÀNG (TỔNG HỢP)</div>', unsafe_allow_html=True)

# --- ĐÂY LÀ CHỖ BẠN YÊU CẦU: 5 BIỂU ĐỒ TRÊN 1 HÀNG ---
mid_1, mid_2, mid_3, mid_4, mid_5 = st.columns(5)

with mid_1:
    st.markdown('**1. Cấu trúc DT**')
    df_market = pd.DataFrame({"Năm": ["23", "24", "25"]*3, "Mảng": ["In", "Out", "Dom"]*3, "Doanh Thu": [200, 500, 300, 250, 600, 350, 400, 800, 500]})
    fig_market = px.bar(df_market, x="Năm", y="Doanh Thu", color="Mảng", text_auto=True, color_discrete_map=COLOR_MAP)
    fig_market.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_market, use_container_width=True)

with mid_2:
    st.markdown('**2. CLV vs CAC**')
    fig_clv = go.Figure()
    fig_clv.add_trace(go.Scatter(name='CLV', x=['Q1','Q2','Q3','Q4'], y=[100,120,150,180], line=dict(color='#0051a3')))
    fig_clv.add_trace(go.Scatter(name='CAC', x=['Q1','Q2','Q3','Q4'], y=[50,55,50,45], line=dict(dash='dot', color='#d62728')))
    fig_clv.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_clv, use_container_width=True)

with mid_3:
    st.markdown('**3. Tăng trưởng**')
    fig_gr = go.Figure()
    fig_gr.add_trace(go.Bar(name='Vietravel', x=['Q1','Q2','Q3'], y=[15,20,25], marker_color='#0051a3', text_auto=True))
    fig_gr.add_trace(go.Scatter(name='Ngành', x=['Q1','Q2','Q3'], y=[10,12,10], line=dict(color='red')))
    fig_gr.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_gr, use_container_width=True)

with mid_4:
    # ROI MARKETING (ĐƯA LÊN ĐÂY)
    st.markdown('**4. ROI MKT**')
    df_mkt = pd.DataFrame({"Kênh": ["FB", "GG", "Tik", "Evt", "Báo"], "Chi phí": [2, 5, 1, 3, 0.5], "Doanh thu": [20, 60, 15, 10, 2]})
    fig_mkt = px.scatter(df_mkt, x="Chi phí", y="Doanh thu", color="Kênh", size="Doanh thu", text="Kênh", color_discrete_map=COLOR_MAP)
    fig_mkt.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_mkt, use_container_width=True)

with mid_5:
    # RMS (ĐƯA LÊN ĐÂY)
    st.markdown('**5. RMS (Khách)**')
    df_rms = pd.DataFrame({"Tuyến": ["ĐBA", "Âu", "ĐNA", "Dom"], "RMS": [0.8, 1.2, 1.5, 0.9], "Gr": [15, 10, 5, 8], "Pax": [15000, 8000, 25000, 40000]})
    fig_bub = px.scatter(df_rms, x="RMS", y="Gr", size="Pax", color="Tuyến", text="Tuyến", color_discrete_map=COLOR_MAP)
    fig_bub.add_vline(x=1, line_dash="dash", line_color="red")
    fig_bub.update_layout(showlegend=False, height=250, margin=dict(l=0, r=0, t=30, b=0), xaxis_title="RMS")
    st.plotly_chart(fig_bub, use_container_width=True)

# ==============================================================================
# HÀNG 3: NHÂN SỰ
# ==============================================================================
st.markdown('<div class="header-style">4. NHÂN SỰ & QUẢN TRỊ RỦI RO</div>', unsafe_allow_html=True)
bot_1, bot_2, bot_3 = st.columns(3)

with bot_1:
    st.markdown('**Năng suất: Lợi nhuận/NS**')
    df_hr = pd.DataFrame({"Năm": ["23", "24", "25"] * 5, "Đơn vị": sorted(["Toàn Cty", "HO", "Bắc", "Trung", "Tây"] * 3), "Lợi nhuận": [180, 200, 220, 200, 230, 250, 150, 170, 190, 160, 180, 200, 120, 130, 140]})
    fig_hr = px.bar(df_hr, x="Năm", y="Lợi nhuận", color="Đơn vị", barmode='group', text_auto=True, color_discrete_map=COLOR_MAP)
    st.plotly_chart(fig_hr, use_container_width=True)

with bot_2:
    st.markdown('**Giữ chân Key Person**')
    st.metric(label="Tỷ lệ giữ chân", value="95%", delta="-2%")
    df_risk = pd.DataFrame({"Khu vực": ["Miền Bắc", "Miền Tây"], "Cảnh báo": ["GĐ CN A", "TP KD B"], "Rủi ro": ["Cao", "TB"]})
    st.dataframe(df_risk.style.applymap(lambda v: 'color: red; font-weight: bold;' if v == 'Cao' else 'color: black'), use_container_width=True)

with bot_3:
    st.markdown('**Sẵn sàng kế thừa (%)**')
    fig_heat = px.imshow([[100, 90, 20], [80, 50, 10], [100, 100, 80]], x=['TP', 'PGĐ', 'GĐ'], y=['Tây', 'Bắc', 'HO'], color_continuous_scale='RdYlGn', text_auto=True) 
    st.plotly_chart(fig_heat, use_container_width=True)
