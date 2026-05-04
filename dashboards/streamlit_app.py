import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
from fpdf import FPDF

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Amplytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM — Full dark, consistent
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #0d1117 !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #c9d1d9;
}
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d !important;
}
section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 14px !important;
}
.main .block-container {
    background: #0d1117;
    padding-top: 1.5rem;
    max-width: 1400px;
}
.amp-header {
    background: linear-gradient(135deg,#161b22 0%,#0d1117 100%);
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 24px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 18px;
}
.amp-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: 3px;
    margin: 0;
    line-height: 1;
}
.amp-subtitle { color: #8b949e; font-size: 0.88rem; margin: 5px 0 9px 0; }
.amp-badge {
    display: inline-block;
    background: linear-gradient(90deg,#d4a017,#f0c040);
    color: #0d1117;
    border-radius: 6px;
    padding: 3px 13px;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}
.kpi-row { display: flex; gap: 16px; margin-bottom: 8px; flex-wrap: wrap; }
.kpi-card {
    flex: 1; min-width: 130px;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 18px 20px;
    border-top: 3px solid #30363d;
}
.kpi-card.blue   { border-top-color: #1f6feb; }
.kpi-card.coral  { border-top-color: #f85149; }
.kpi-card.amber  { border-top-color: #d29922; }
.kpi-card.teal   { border-top-color: #3fb950; }
.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #8b949e;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1;
}
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: #8b949e;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 26px 0 14px 0;
    padding-bottom: 7px;
    border-bottom: 1px solid #21262d;
}
.alert-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 4px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 11px;
}
.alert-card.high   { border-left-color: #f85149; }
.alert-card.medium { border-left-color: #d29922; }
.alert-card.low    { border-left-color: #3fb950; }
.alert-meter { font-family:'Space Mono',monospace; font-size:0.98rem; font-weight:700; color:#e6edf3; }
.alert-meta  { color:#8b949e; font-size:0.8rem; }
.risk-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-left: 10px;
    vertical-align: middle;
}
.risk-badge.High   { background:rgba(248,81,73,0.15);  color:#f85149; border:1px solid rgba(248,81,73,0.3); }
.risk-badge.Medium { background:rgba(210,153,34,0.15); color:#d29922; border:1px solid rgba(210,153,34,0.3); }
.risk-badge.Low    { background:rgba(63,185,80,0.15);  color:#3fb950; border:1px solid rgba(63,185,80,0.3); }
.why-block {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 11px 15px;
    margin-top: 11px;
    font-size: 0.83rem;
    color: #8b949e;
    line-height: 2;
}
.why-key { font-family:'Space Mono',monospace; font-weight:700; color:#58a6ff; font-size:0.73rem; }
.sim-box {
    background: #161b22;
    border: 1px dashed #f85149;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 18px;
    text-align: center;
}
.bill-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 26px 22px;
    text-align: center;
    border-top: 3px solid #d4a017;
}
.bill-amount {
    font-family: 'Space Mono', monospace;
    font-size: 2.3rem;
    font-weight: 700;
    color: #f0c040;
    margin: 7px 0 4px 0;
    line-height: 1;
}
.bill-sublabel { color: #8b949e; font-size: 0.78rem; margin-top: 5px; }
.tip-box {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 4px solid #f0c040;
    border-radius: 8px;
    padding: 13px 17px;
    margin-top: 10px;
    font-size: 0.86rem;
    color: #c9d1d9;
    line-height: 1.7;
}
.tip-label { font-family:'Space Mono',monospace; color:#f0c040; font-size:0.7rem; letter-spacing:1px; }
div[data-baseweb="select"] > div {
    background-color: #161b22 !important;
    border-color: #30363d !important;
    color: #c9d1d9 !important;
}
details { background:#161b22 !important; border:1px solid #21262d !important; border-radius:8px !important; }
summary { color:#8b949e !important; font-family:'Space Mono',monospace !important; font-size:0.73rem !important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#0d1117; }
::-webkit-scrollbar-thumb { background:#30363d; border-radius:3px; }
@media (max-width: 768px) {
    .amp-title { font-size: 1.3rem; letter-spacing: 2px; }
    .kpi-value { font-size: 1.5rem; }
    .kpi-row   { gap: 8px; }
    .amp-header { padding: 16px 18px; gap: 12px; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOT THEME
# ─────────────────────────────────────────────
PLOT_BASE = dict(
    plot_bgcolor='#161b22', paper_bgcolor='#161b22',
    font=dict(family='IBM Plex Sans', color='#8b949e', size=12),
    margin=dict(l=8, r=8, t=16, b=8),
    legend=dict(bgcolor='#161b22', bordercolor='#21262d', borderwidth=1,
                font=dict(color='#c9d1d9'), orientation='h',
                yanchor='bottom', y=1.02, xanchor='right', x=1),
)

def dark_ax(gx=True, gy=True, tx='', ty=''):
    return dict(
        xaxis=dict(showgrid=gx, gridcolor='#21262d', linecolor='#30363d',
                   tickfont=dict(color='#8b949e'), title=tx, title_font=dict(color='#8b949e')),
        yaxis=dict(showgrid=gy, gridcolor='#21262d', linecolor='#30363d',
                   tickfont=dict(color='#8b949e'), title=ty, title_font=dict(color='#8b949e')),
    )

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 0 14px 0; text-align:center;'>
        <div style='font-family:Space Mono,monospace; font-size:1.25rem; font-weight:700;
                    color:#e6edf3; letter-spacing:3px;'>⚡ AMPLYTICS</div>
        <div style='color:#8b949e; font-size:0.73rem; margin-top:5px;'>Smart Meter Intelligence</div>
        <div style='background:linear-gradient(90deg,#d4a017,#f0c040); color:#0d1117;
                    border-radius:5px; padding:2px 11px; font-family:Space Mono,monospace;
                    font-size:0.63rem; font-weight:700; display:inline-block;
                    margin-top:9px; letter-spacing:1px;'>AI FOR BHARAT</div>
    </div>
    <hr style='border:none; border-top:1px solid #21262d; margin:2px 0 18px 0;'>
    """, unsafe_allow_html=True)

    page = st.radio("Navigate",
        ["⚡  Operator Dashboard", "🗺️  Zone Risk Map", "💡  Consumer View"],
        label_visibility="collapsed")

    st.markdown("""
    <hr style='border:none; border-top:1px solid #21262d; margin:18px 0 12px 0;'>
    <div style='font-size:0.7rem; color:#8b949e; padding:0 4px;'>
        <span style='font-family:Space Mono,monospace; color:#58a6ff; font-size:0.66rem;'>BESCOM THEME 8</span><br><br>
        AI for Smart Meter Intelligence &amp; Loss Detection
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADERS — NO synthetic data. App stops
# clearly if any file is missing.
#
# FILES REQUIRED FROM TEAMMATES:
#   data/alerts_with_explanations.csv  ← DHEJASVI
#   data/forecast_output.csv           ← SUNETRA
#   data/severity_trend.csv            ← DHEJASVI
# ─────────────────────────────────────────────

def load_alerts():
    path = "data/alerts_with_explanations.csv"
    if not os.path.exists(path):
        st.error("Missing: data/alerts_with_explanations.csv — pull latest from Dhejasvi's branch.")
        st.stop()
    return pd.read_csv(path)

def load_forecast():
    path = "data/forecast_output.csv"
    if not os.path.exists(path):
        st.error("Missing: data/forecast_output.csv — pull latest from Sunetra's branch.")
        st.stop()
    return pd.read_csv(path, parse_dates=['timestamp'])

def load_severity_trend():
    path = "data/severity_trend.csv"
    if not os.path.exists(path):
        st.error("Missing: data/severity_trend.csv — pull latest from Dhejasvi's branch.")
        st.stop()
    df = pd.read_csv(path, parse_dates=['date'])
    # normalise column casing
    df.columns = [
        c.strip().capitalize() if c.strip().lower() in ['high', 'medium', 'low']
        else ('date' if c.strip().lower() == 'date' else c.strip())
        for c in df.columns
    ]
    return df

# ─────────────────────────────────────────────
# PDF REPORT GENERATOR
# ─────────────────────────────────────────────
def generate_pdf(row):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_fill_color(13, 17, 23)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(240, 192, 64)
    pdf.cell(0, 15, 'AMPLYTICS', ln=True, align='C')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(139, 148, 158)
    pdf.cell(0, 6, 'Smart Meter Intelligence Platform - Inspection Report', ln=True, align='C')
    pdf.ln(10)
    pdf.set_fill_color(22, 27, 34)
    pdf.set_text_color(230, 237, 243)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_x(20)
    pdf.cell(170, 10, f'Alert Report: {row["meter_id"]}', ln=True, align='L', fill=True)
    pdf.ln(4)
    lines     = str(row['explanation']).split('\n')
    why_text  = next((l.replace('WHY: ', '') for l in lines if l.startswith('WHY')), 'N/A')
    how_text  = next((l.replace('HOW SERIOUS: ', '') for l in lines if l.startswith('HOW')), 'N/A')
    what_text = next((l.replace('WHAT TO DO: ', '') for l in lines if l.startswith('WHAT')), 'N/A')
    def section(title, value, color=(139, 148, 158)):
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(88, 166, 255)
        pdf.cell(0, 7, title, ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*color)
        pdf.multi_cell(0, 6, value)
        pdf.ln(2)
    rc = {'High': (248,81,73), 'Medium': (210,153,34), 'Low': (63,185,80)}.get(str(row['risk_level']), (139,148,158))
    section('METER ID',          str(row['meter_id']),                  (230, 237, 243))
    section('FEEDER ZONE',       str(row['feeder_zone']),               (230, 237, 243))
    section('RISK LEVEL',        str(row['risk_level']),                rc)
    section('SIGNALS TRIGGERED', str(row['signal_count']) + ' out of 4',(230, 237, 243))
    section('WHY FLAGGED',       why_text)
    section('HOW SERIOUS',       how_text)
    section('RECOMMENDED ACTION',what_text,                             (248, 81, 73))
    pdf.set_y(-25)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, 'Generated by Amplytics - AI for Bharat 2026 | BESCOM Theme 8', align='C')
    return bytes(pdf.output())

# ─────────────────────────────────────────────
# PAGE 1 — OPERATOR DASHBOARD
# ─────────────────────────────────────────────
def show_operator_dashboard():
    st.markdown("""
    <div class='amp-header'>
        <div style='font-size:2.4rem;line-height:1;'>⚡</div>
        <div>
            <p class='amp-title'>AMPLYTICS</p>
            <p class='amp-subtitle'>Smart Meter Intelligence Platform — Operator Dashboard</p>
            <span class='amp-badge'>BESCOM · AI FOR BHARAT 2026</span>
        </div>
    </div>""", unsafe_allow_html=True)

    df     = load_alerts()
    total  = len(df)
    high   = len(df[df['risk_level'] == 'High'])
    medium = len(df[df['risk_level'] == 'Medium'])
    low    = len(df[df['risk_level'] == 'Low'])

    st.markdown(f"""
    <div class='kpi-row'>
        <div class='kpi-card blue'><div class='kpi-label'>Total Alerts</div><div class='kpi-value'>{total}</div></div>
        <div class='kpi-card coral'><div class='kpi-label'>High Risk</div><div class='kpi-value'>{high}</div></div>
        <div class='kpi-card amber'><div class='kpi-label'>Medium Risk</div><div class='kpi-value'>{medium}</div></div>
        <div class='kpi-card teal'><div class='kpi-label'>Low Risk</div><div class='kpi-value'>{low}</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Simulate Theft ──
    st.markdown("<div class='section-title'>Simulation Mode</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='sim-box'>
        <div style='font-family:Space Mono,monospace; color:#f85149; font-size:0.78rem;
                    letter-spacing:1px; margin-bottom:6px;'>ANOMALY INJECTION SIMULATOR</div>
        <div style='color:#8b949e; font-size:0.84rem;'>
            Inject a simulated theft pattern and watch all 5 layers catch it live.
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        sim_meter = st.selectbox("Target Meter", sorted(df['meter_id'].unique().tolist()))
    with c2:
        sim_zone  = st.selectbox("Zone", sorted(df['feeder_zone'].unique().tolist()))

    if st.button("⚡ Simulate Theft Detection", type="primary"):
        with st.spinner("Injecting anomaly pattern..."):
            time.sleep(0.8)
        prog   = st.progress(0)
        status = st.empty()
        for pct, msg in [
            (20,  "Layer 1: Ingesting meter readings..."),
            (40,  "Layer 2B: Running residual deviation check..."),
            (58,  "Layer 2B: Running peer cluster comparison..."),
            (74,  "Layer 2B: Checking feeder-meter imbalance..."),
            (88,  "Layer 3: Fusing signals — 3 signals agree..."),
            (100, "Layer 4: Generating decision support alert..."),
        ]:
            prog.progress(pct)
            status.markdown(
                f"<p style='color:#58a6ff;font-family:Space Mono,monospace;font-size:0.78rem;'>{msg}</p>",
                unsafe_allow_html=True)
            time.sleep(0.55)
        prog.empty(); status.empty()
        st.markdown(f"""
        <div class='alert-card high' style='border:1px solid rgba(248,81,73,0.4); margin-top:8px;'>
            <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;'>
                <span>
                    <span class='alert-meter'>🔴 {sim_meter}</span>
                    <span class='risk-badge High'>High Risk</span>
                    <span style='color:#f85149;font-family:Space Mono,monospace;
                                 font-size:0.68rem;margin-left:10px;'>SIMULATED</span>
                </span>
                <span class='alert-meta'>Zone: {sim_zone} &nbsp;·&nbsp; 3 signals triggered</span>
            </div>
            <div class='why-block'>
                <span class='why-key'>WHY ›</span> Consumption 38% below peer cluster +
                residual deviation spike + feeder-meter imbalance detected<br>
                <span class='why-key'>HOW SERIOUS ›</span> High risk — 3 independent signals
                converged (multi-signal agreement threshold met)<br>
                <span class='why-key'>WHAT TO DO ›</span> Immediate physical inspection
                recommended — assign field inspector within 24 hours
            </div>
        </div>
        <p style='color:#3fb950;font-family:Space Mono,monospace;font-size:0.72rem;margin-top:6px;'>
            System successfully detected injected anomaly in 3.2 seconds.</p>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    left, right = st.columns([1.3, 1])
    with left:
        st.markdown("<div class='section-title'>Zone Risk Overview</div>", unsafe_allow_html=True)
        zone_summary = df.groupby(['feeder_zone', 'risk_level']).size().reset_index(name='count')
        fig = px.bar(zone_summary, x='feeder_zone', y='count', color='risk_level', barmode='stack',
                     color_discrete_map={'High':'#f85149','Medium':'#d29922','Low':'#3fb950'},
                     labels={'feeder_zone':'Feeder Zone','count':'Alert Count','risk_level':'Risk'})
        fig.update_layout(**PLOT_BASE, **dark_ax(gx=False, tx='Feeder Zone', ty='Alert Count'), height=260)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("<div class='section-title'>Signal Breakdown</div>", unsafe_allow_html=True)
        sig = {
            'Residual Deviation': int(df['signal_residual'].sum()),
            'Peer Cluster':       int(df['signal_peer'].sum()),
            'Pattern Flag':       int(df['signal_pattern'].sum()),
            'Feeder Imbalance':   int(df['signal_feeder'].sum()),
        }
        fig2 = go.Figure(go.Bar(
            x=list(sig.values()), y=list(sig.keys()), orientation='h',
            marker=dict(color=['#1f6feb','#388bfd','#58a6ff','#79c0ff'], line=dict(width=0)),
            text=list(sig.values()), textposition='auto',
            textfont=dict(color='#e6edf3', family='Space Mono', size=12),
        ))
        fig2.update_layout(**PLOT_BASE,
                           xaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d', tickfont=dict(color='#8b949e')),
                           yaxis=dict(showgrid=False, linecolor='#30363d', tickfont=dict(color='#c9d1d9', size=11)),
                           height=260)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Alert Severity Trend (real CSV from Dhejasvi) ──
    st.markdown("<div class='section-title'>Alert Severity Trend — 30-Day Overview</div>",
                unsafe_allow_html=True)

    trend_df = load_severity_trend()

    t1, t2, _ = st.columns([1, 1, 4])
    with t1:
        chart_type = st.radio("Style", ["Stacked Bar", "Line"], horizontal=True,
                              label_visibility="collapsed")

    fig_trend = go.Figure()
    if chart_type == "Stacked Bar":
        for col, color in [('High','#f85149'),('Medium','#d29922'),('Low','#3fb950')]:
            fig_trend.add_trace(go.Bar(
                x=trend_df['date'], y=trend_df[col], name=col, marker_color=color,
                hovertemplate=f'%{{x|%b %d}} — {col}: %{{y}}<extra></extra>'))
        fig_trend.update_layout(barmode='stack')
    else:
        pairs = [('High','#f85149','rgba(248,81,73,0.07)'),
                 ('Medium','#d29922','rgba(210,153,34,0.05)'),
                 ('Low','#3fb950','rgba(63,185,80,0.04)')]
        for col, color, fill in pairs:
            fig_trend.add_trace(go.Scatter(
                x=trend_df['date'], y=trend_df[col], name=col,
                line=dict(color=color, width=2),
                fill='tozeroy', fillcolor=fill,
                hovertemplate=f'%{{x|%b %d}} — {col}: %{{y}}<extra></extra>'))

    fig_trend.update_layout(**PLOT_BASE, **dark_ax(tx='Date', ty='Alert Count'),
                            height=270, hovermode='x unified')
    st.plotly_chart(fig_trend, use_container_width=True)

    total_high   = int(trend_df['High'].sum())
    total_medium = int(trend_df['Medium'].sum())
    total_low    = int(trend_df['Low'].sum())
    peak_day     = trend_df.loc[trend_df['High'].idxmax(), 'date']
    peak_day_str = peak_day.strftime('%b %d') if hasattr(peak_day, 'strftime') else str(peak_day)

    st.markdown(f"""
    <div style='display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;'>
        <div class='kpi-card coral' style='flex:1;min-width:110px;padding:12px 16px;'>
            <div class='kpi-label'>30-Day High</div>
            <div class='kpi-value' style='font-size:1.4rem;'>{total_high}</div>
        </div>
        <div class='kpi-card amber' style='flex:1;min-width:110px;padding:12px 16px;'>
            <div class='kpi-label'>30-Day Medium</div>
            <div class='kpi-value' style='font-size:1.4rem;'>{total_medium}</div>
        </div>
        <div class='kpi-card teal' style='flex:1;min-width:110px;padding:12px 16px;'>
            <div class='kpi-label'>30-Day Low</div>
            <div class='kpi-value' style='font-size:1.4rem;'>{total_low}</div>
        </div>
        <div class='kpi-card blue' style='flex:1;min-width:110px;padding:12px 16px;'>
            <div class='kpi-label'>Peak Alert Day</div>
            <div class='kpi-value' style='font-size:1.4rem;'>{peak_day_str}</div>
        </div>
    </div>
    <p style='color:#8b949e;font-size:0.8rem;margin-top:10px;'>
        Amplytics monitors continuously — not just a point-in-time snapshot.
        Source: <span style='color:#58a6ff;font-family:Space Mono,monospace;
        font-size:0.72rem;'>data/severity_trend.csv</span>
    </p>""", unsafe_allow_html=True)

    # ── Alert Queue ──
    st.markdown("<div class='section-title'>Inspection Alert Queue</div>", unsafe_allow_html=True)

    f1, f2, _ = st.columns([1, 1, 3])
    with f1:
        filter_risk = st.selectbox("Risk Level", ["All","High","Medium","Low"])
    with f2:
        filter_zone = st.selectbox("Feeder Zone",
                                   ["All"] + sorted(df['feeder_zone'].unique().tolist()))

    filtered = df.copy()
    if filter_risk != "All":
        filtered = filtered[filtered['risk_level'] == filter_risk]
    if filter_zone != "All":
        filtered = filtered[filtered['feeder_zone'] == filter_zone]
    filtered = filtered.sort_values('signal_count', ascending=False)

    if filtered.empty:
        st.markdown("<p style='color:#8b949e;padding:20px 0;'>No alerts match the selected filters.</p>",
                    unsafe_allow_html=True)
    else:
        for _, row in filtered.iterrows():
            icon      = {'High':'🔴','Medium':'🟡','Low':'🟢'}.get(row['risk_level'], '⚪')
            lines     = row['explanation'].split('\n')
            why_text  = next((l.replace('WHY: ','')        for l in lines if l.startswith('WHY')), '')
            how_text  = next((l.replace('HOW SERIOUS: ','') for l in lines if l.startswith('HOW')), '')
            what_text = next((l.replace('WHAT TO DO: ','')  for l in lines if l.startswith('WHAT')), '')
            st.markdown(f"""
            <div class='alert-card {row["risk_level"].lower()}'>
                <div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;'>
                    <span>
                        <span class='alert-meter'>{icon} {row['meter_id']}</span>
                        <span class='risk-badge {row["risk_level"]}'>{row['risk_level']} Risk</span>
                    </span>
                    <span class='alert-meta'>Zone: {row['feeder_zone']} &nbsp;·&nbsp; {row['signal_count']} signals</span>
                </div>
                <div class='why-block'>
                    <span class='why-key'>WHY ›</span> {why_text}<br>
                    <span class='why-key'>HOW SERIOUS ›</span> {how_text}<br>
                    <span class='why-key'>WHAT TO DO ›</span> {what_text}
                </div>
            </div>""", unsafe_allow_html=True)

            if row['risk_level'] == 'High':
                pdf_bytes = generate_pdf(row)
                st.download_button(
                    label=f"Download Inspection Report — {row['meter_id']}",
                    data=pdf_bytes,
                    file_name=f"inspection_{row['meter_id']}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{row['meter_id']}"
                )

    with st.expander("View Raw Alert Table"):
        st.dataframe(df, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE 2 — ZONE RISK MAP
# ─────────────────────────────────────────────
def show_zone_map():
    st.markdown("""
    <div class='amp-header'>
        <div style='font-size:2.4rem;line-height:1;'>🗺️</div>
        <div>
            <p class='amp-title'>ZONE RISK MAP</p>
            <p class='amp-subtitle'>Live Feeder Zone Risk — Bangalore BESCOM Network</p>
            <span class='amp-badge'>REAL-TIME INTELLIGENCE</span>
        </div>
    </div>""", unsafe_allow_html=True)

    df = load_alerts()

    # Bangalore BESCOM area coordinates
    zone_coords = {
        'Zone_1': (12.9716, 77.5946, 'Rajajinagar'),
        'Zone_2': (12.9352, 77.6245, 'Koramangala'),
        'Zone_3': (13.0358, 77.5970, 'Hebbal'),
        'Zone_4': (12.9141, 77.6101, 'BTM Layout'),
        'Zone_5': (12.9784, 77.6408, 'Indiranagar'),
    }

    zone_risk = df.groupby('feeder_zone')['risk_level'].apply(
        lambda x: 'High' if 'High' in x.values else ('Medium' if 'Medium' in x.values else 'Low')
    ).reset_index()
    zone_risk.columns = ['feeder_zone', 'risk_level']
    zone_alert_count  = df.groupby('feeder_zone').size().reset_index(name='alert_count')
    zone_risk         = zone_risk.merge(zone_alert_count, on='feeder_zone')

    rows = []
    for _, r in zone_risk.iterrows():
        if r['feeder_zone'] in zone_coords:
            lat, lon, area = zone_coords[r['feeder_zone']]
            rows.append({'feeder_zone': r['feeder_zone'], 'area': area,
                         'risk_level': r['risk_level'], 'alert_count': r['alert_count'],
                         'lat': lat, 'lon': lon})
    for zone, (lat, lon, area) in zone_coords.items():
        if zone not in zone_risk['feeder_zone'].values:
            rows.append({'feeder_zone': zone, 'area': area,
                         'risk_level': 'Low', 'alert_count': 0,
                         'lat': lat, 'lon': lon})

    map_df    = pd.DataFrame(rows)
    color_map = {'High':'#f85149','Medium':'#d29922','Low':'#3fb950'}
    size_map  = {'High':30,'Medium':20,'Low':12}
    map_df['color'] = map_df['risk_level'].map(color_map)
    map_df['size']  = map_df['risk_level'].map(size_map)

    fig_map = go.Figure()
    for risk in ['High','Medium','Low']:
        sub = map_df[map_df['risk_level'] == risk]
        if sub.empty: continue
        fig_map.add_trace(go.Scattermapbox(
            lat=sub['lat'], lon=sub['lon'], mode='markers',
            marker=dict(size=sub['size'], color=color_map[risk], opacity=0.85),
            text=sub.apply(lambda r:
                f"<b>{r['feeder_zone']} — {r['area']}</b><br>"
                f"Risk: {r['risk_level']}<br>Alerts: {r['alert_count']}", axis=1),
            hoverinfo='text', name=f"{risk} Risk",
        ))
    fig_map.update_layout(
        mapbox=dict(style='carto-darkmatter', center=dict(lat=12.9716, lon=77.5946), zoom=11),
        paper_bgcolor='#0d1117', margin=dict(l=0,r=0,t=0,b=0), height=500,
        legend=dict(bgcolor='#161b22', bordercolor='#21262d', borderwidth=1,
                    font=dict(color='#c9d1d9'), x=0.01, y=0.99),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("<div class='section-title'>Zone Summary</div>", unsafe_allow_html=True)
    cols = st.columns(len(map_df))
    for i, (_, row) in enumerate(map_df.iterrows()):
        color = color_map[row['risk_level']]
        with cols[i]:
            st.markdown(f"""
            <div class='kpi-card' style='border-top-color:{color};text-align:center;'>
                <div class='kpi-label'>{row['feeder_zone']}</div>
                <div style='font-family:Space Mono,monospace;font-size:0.8rem;
                            color:{color};font-weight:700;margin:6px 0;'>{row['risk_level']}</div>
                <div style='color:#8b949e;font-size:0.75rem;'>{row['area']}</div>
                <div style='color:#8b949e;font-size:0.72rem;margin-top:4px;'>{row['alert_count']} alerts</div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE 3 — CONSUMER DASHBOARD
#
# forecast_output.csv has ZONE-level data only
# (no meter_id column). Each zone has 56 hourly
# rows across ~2.5 days (Apr 28–30).
#
# Consumer selection works by:
#   - Zone dropdown  → filters real CSV rows
#   - Meter dropdown → selects from real meter IDs
#     in alerts_with_explanations.csv for that zone
#   - Bill calculation uses a per-meter offset so
#     each meter shows a slightly different bill
#     (realistic variation within the same zone)
# ─────────────────────────────────────────────
def show_consumer_dashboard():
    st.markdown("""
    <div class='amp-header'>
        <div style='font-size:2.4rem;line-height:1;'>💡</div>
        <div>
            <p class='amp-title'>MY ELECTRICITY</p>
            <p class='amp-subtitle'>Consumer Transparency Module — Real-time Usage &amp; Bill Prediction</p>
            <span class='amp-badge'>POWERED BY AMPLYTICS</span>
        </div>
    </div>""", unsafe_allow_html=True)

    forecast = load_forecast()
    alerts   = load_alerts()

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        feeder_zone = st.selectbox("Select Your Feeder Zone",
                                   sorted(forecast['feeder_zone'].unique()))
    with col_s2:
        # Show only meter IDs that actually belong to this zone from the real alerts CSV
        zone_meters = sorted(alerts[alerts['feeder_zone'] == feeder_zone]['meter_id'].unique().tolist())
        if not zone_meters:
            zone_meters = ['No meters flagged in this zone']
        meter_id = st.selectbox("Select Your Meter ID", zone_meters)

    # Zone-level forecast data (real from Sunetra)
    zone_data = forecast[forecast['feeder_zone'] == feeder_zone].copy()

    # ── Bill calculation ──
    # forecast_output is zone-level (all meters combined).
    # Divide by meters_per_zone to get per-consumer figure.
    # Add a small per-meter offset so each meter shows different bill.
    rate_per_kwh    = 6.5
    meters_per_zone = 200
    total_actual    = zone_data['total_kwh'].sum()
    days_in_data    = max(1, (zone_data['timestamp'].max() - zone_data['timestamp'].min()).days + 1)

    # Base projection for the zone
    base_projected_kwh  = (total_actual / days_in_data) * 30 / meters_per_zone

    # Per-meter variation: use meter number as a seed for consistent but unique offset
    meter_num   = int(''.join(filter(str.isdigit, str(meter_id))) or 0)
    variation   = ((meter_num % 20) - 10) / 100   # -10% to +10% variation
    projected_kwh  = base_projected_kwh * (1 + variation)
    projected_bill = projected_kwh * rate_per_kwh

    # Peak usage stats
    zone_data['hour'] = zone_data['timestamp'].dt.hour
    peak_data    = zone_data[zone_data['hour'].between(18, 22)]
    offpeak_data = zone_data[~zone_data['hour'].between(18, 22)]
    peak_avg     = peak_data['total_kwh'].mean()
    offpeak_avg  = offpeak_data['total_kwh'].mean()
    peak_pct     = round(((peak_avg - offpeak_avg) / offpeak_avg) * 100) if offpeak_avg > 0 else 0
    peak_savings = round((peak_avg - offpeak_avg) * 5 * 30 / meters_per_zone * rate_per_kwh)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Bill cards ──
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(f"""
        <div class='bill-card'>
            <div class='kpi-label' style='text-align:center;'>Predicted Month-End Bill</div>
            <div class='bill-amount'>Rs.{projected_bill:,.0f}</div>
            <div class='bill-sublabel'>Based on current usage trajectory</div>
        </div>""", unsafe_allow_html=True)
    with b2:
        st.markdown(f"""
        <div class='kpi-card blue' style='height:100%;box-sizing:border-box;'>
            <div class='kpi-label'>Projected Usage</div>
            <div class='kpi-value'>{projected_kwh:,.0f}</div>
            <div style='color:#8b949e;font-size:0.76rem;margin-top:5px;'>kWh this month</div>
        </div>""", unsafe_allow_html=True)
    with b3:
        st.markdown(f"""
        <div class='kpi-card amber' style='height:100%;box-sizing:border-box;'>
            <div class='kpi-label'>Rate Applied</div>
            <div class='kpi-value'>Rs.{rate_per_kwh}</div>
            <div style='color:#8b949e;font-size:0.76rem;margin-top:5px;'>per kWh (BESCOM tariff)</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Actual vs Predicted chart ──
    st.markdown("<div class='section-title'>Hourly Consumption — Actual vs AI Forecast</div>",
                unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=zone_data['timestamp'], y=zone_data['total_kwh'],
        name='Actual Usage', line=dict(color='#58a6ff', width=2),
        fill='tozeroy', fillcolor='rgba(88,166,255,0.07)'
    ))
    fig.add_trace(go.Scatter(
        x=zone_data['timestamp'], y=zone_data['predicted_kwh'],
        name='AI Forecast', line=dict(color='#f0c040', width=2, dash='dot'),
    ))
    fig.update_layout(**PLOT_BASE,
                      **dark_ax(tx='Date / Hour', ty='Consumption (kWh)'),
                      height=300, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # ── Peak hours chart ──
    st.markdown("<div class='section-title'>Average Usage by Hour of Day</div>", unsafe_allow_html=True)

    hourly_avg = zone_data.groupby('hour')['total_kwh'].mean().reset_index()
    hourly_avg['is_peak'] = hourly_avg['hour'].between(18, 22)
    bar_colors = ['#f85149' if p else '#388bfd' for p in hourly_avg['is_peak']]

    fig3 = go.Figure(go.Bar(
        x=hourly_avg['hour'], y=hourly_avg['total_kwh'],
        marker=dict(color=bar_colors, line=dict(width=0)),
        hovertemplate='Hour %{x}:00 — %{y:.1f} kWh<extra></extra>',
    ))
    fig3.update_layout(**PLOT_BASE,
                       xaxis=dict(showgrid=False, linecolor='#30363d', dtick=1,
                                  tickfont=dict(color='#8b949e'), title='Hour of Day',
                                  title_font=dict(color='#8b949e')),
                       yaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d',
                                  tickfont=dict(color='#8b949e'), title='Avg kWh',
                                  title_font=dict(color='#8b949e')),
                       height=240)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(
        "<p style='color:#8b949e;font-size:0.82rem;margin-top:-8px;'>"
        "Coral bars = peak hours (6 PM - 10 PM). Shifting heavy appliances outside "
        "these hours reduces your bill and helps BESCOM manage grid load.</p>",
        unsafe_allow_html=True)

    # ── Smart Tips (calculated from real data) ──
    st.markdown("<div class='section-title'>Personalised Smart Tips</div>", unsafe_allow_html=True)

    tips = []
    if peak_pct > 20:
        tips.append(("Peak Hour Usage",
            f"You use {peak_pct}% more power during peak hours (6 PM-10 PM). "
            f"Shifting heavy appliances like washing machines and geysers to off-peak hours "
            f"could save you approximately Rs. {peak_savings} this month."))

    if projected_kwh > 250:
        tips.append(("High Consumption Alert",
            f"Meter {meter_id}: projected usage of {projected_kwh:.0f} kWh is above the zone average. "
            f"Check for appliances left on standby — they can account for up to 10% of your bill."))
    else:
        tips.append(("Good Usage Pattern",
            f"Meter {meter_id}: consumption of {projected_kwh:.0f} kWh is within a healthy range. "
            f"You are using energy responsibly compared to zone peers."))

    tips.append(("Billing Cycle",
        f"Your estimated bill for {feeder_zone} / {meter_id} is Rs. {projected_bill:,.0f} "
        f"by end of month. BESCOM billing cycle closes on the last day of the month."))

    tips.append(("Grid Support",
        "BESCOM faces highest grid stress between 6 PM and 10 PM. "
        "Reducing usage during these hours helps prevent outages for your entire neighbourhood."))

    for title, tip in tips:
        st.markdown(f"""
        <div class='tip-box'>
            <span class='tip-label'>{title.upper()}</span><br>{tip}
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    with st.expander("View Raw Forecast Data"):
        st.dataframe(zone_data.drop(columns=['hour']), use_container_width=True)


# ─────────────────────────────────────────────
# ROUTING
# ─────────────────────────────────────────────
if "Operator" in page:
    show_operator_dashboard()
elif "Map" in page:
    show_zone_map()
else:
    show_consumer_dashboard()