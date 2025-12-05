import streamlit as st
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
    st.plotly_chart(fig_heat, use_container_width=True)
