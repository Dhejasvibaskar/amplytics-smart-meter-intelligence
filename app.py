import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

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
# DESIGN SYSTEM
# Full dark theme throughout — no mixed light/dark
# Typography: Space Mono (headings/labels) + IBM Plex Sans (body)
# Palette: #0d1117 bg, #161b22 cards, #58a6ff blue, #f85149 coral,
#          #d29922 amber, #3fb950 green, #f0c040 gold accent
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

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
    padding-top: 2rem;
    max-width: 1400px;
}

/* Header */
.amp-header {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.amp-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: 3px;
    margin: 0;
    line-height: 1;
}
.amp-subtitle { color: #8b949e; font-size: 0.9rem; margin: 6px 0 10px 0; }
.amp-badge {
    display: inline-block;
    background: linear-gradient(90deg, #d4a017, #f0c040);
    color: #0d1117;
    border-radius: 6px;
    padding: 3px 14px;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}

/* KPI Cards */
.kpi-row { display: flex; gap: 16px; margin-bottom: 8px; }
.kpi-card {
    flex: 1;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 20px 24px;
    border-top: 3px solid #30363d;
}
.kpi-card.blue   { border-top-color: #1f6feb; }
.kpi-card.coral  { border-top-color: #f85149; }
.kpi-card.amber  { border-top-color: #d29922; }
.kpi-card.teal   { border-top-color: #3fb950; }
.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #8b949e;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1;
}

/* Section title */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    color: #8b949e;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 28px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #21262d;
}

/* Alert Cards */
.alert-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 4px solid #30363d;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 12px;
}
.alert-card.high   { border-left-color: #f85149; }
.alert-card.medium { border-left-color: #d29922; }
.alert-card.low    { border-left-color: #3fb950; }
.alert-meter {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #e6edf3;
}
.alert-meta { color: #8b949e; font-size: 0.82rem; }
.risk-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
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
    padding: 12px 16px;
    margin-top: 12px;
    font-size: 0.85rem;
    color: #8b949e;
    line-height: 2;
}
.why-key {
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    color: #58a6ff;
    font-size: 0.75rem;
}

/* Bill Card */
.bill-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 28px 24px;
    text-align: center;
    border-top: 3px solid #d4a017;
}
.bill-amount {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: #f0c040;
    margin: 8px 0 4px 0;
    line-height: 1;
}
.bill-sublabel { color: #8b949e; font-size: 0.8rem; margin-top: 6px; }

/* Selects */
div[data-baseweb="select"] > div {
    background-color: #161b22 !important;
    border-color: #30363d !important;
    color: #c9d1d9 !important;
}

/* Expanders */
details {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
}
summary { color: #8b949e !important; font-family: 'Space Mono',monospace !important; font-size:0.75rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#0d1117; }
::-webkit-scrollbar-thumb { background:#30363d; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SHARED PLOT THEME
# ─────────────────────────────────────────────
PLOT_BASE = dict(
    plot_bgcolor='#161b22',
    paper_bgcolor='#161b22',
    font=dict(family='IBM Plex Sans', color='#8b949e', size=12),
    margin=dict(l=8, r=8, t=16, b=8),
    legend=dict(
        bgcolor='#161b22', bordercolor='#21262d', borderwidth=1,
        font=dict(color='#c9d1d9'), orientation='h',
        yanchor='bottom', y=1.02, xanchor='right', x=1
    ),
)

def dark_axes(title_x='', title_y=''):
    return dict(
        xaxis=dict(showgrid=False, linecolor='#30363d',
                   tickfont=dict(color='#8b949e'),
                   title=title_x, title_font=dict(color='#8b949e')),
        yaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d',
                   tickfont=dict(color='#8b949e'),
                   title=title_y, title_font=dict(color='#8b949e')),
    )

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 16px 0; text-align:center;'>
        <div style='font-family:Space Mono,monospace; font-size:1.3rem; font-weight:700;
                    color:#e6edf3; letter-spacing:3px;'>⚡ AMPLYTICS</div>
        <div style='color:#8b949e; font-size:0.75rem; margin-top:5px;
                    font-family:IBM Plex Sans,sans-serif;'>Smart Meter Intelligence</div>
        <div style='background:linear-gradient(90deg,#d4a017,#f0c040); color:#0d1117;
                    border-radius:5px; padding:3px 12px; font-family:Space Mono,monospace;
                    font-size:0.65rem; font-weight:700; display:inline-block;
                    margin-top:10px; letter-spacing:1px;'>AI FOR BHARAT</div>
    </div>
    <hr style='border:none; border-top:1px solid #21262d; margin:4px 0 20px 0;'>
    """, unsafe_allow_html=True)

    page = st.radio("Navigate",
                    ["⚡  Operator Dashboard", "💡  Consumer View"],
                    label_visibility="collapsed")

    st.markdown("""
    <hr style='border:none; border-top:1px solid #21262d; margin:20px 0 14px 0;'>
    <div style='font-size:0.72rem; color:#8b949e; padding:0 4px;
                font-family:IBM Plex Sans,sans-serif;'>
        <span style='font-family:Space Mono,monospace; color:#58a6ff; font-size:0.68rem;'>
            BESCOM THEME 8</span><br><br>
        AI for Smart Meter Intelligence &amp; Loss Detection
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADERS
# ─────────────────────────────────────────────
def load_alerts():
    path = "data/alerts_with_explanations.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame({
        'meter_id':        ['MTR_0005','MTR_0010','MTR_0015','MTR_0020','MTR_0025'],
        'feeder_zone':     ['Zone_1','Zone_2','Zone_1','Zone_3','Zone_2'],
        'signal_residual': [1,0,1,1,1],
        'signal_peer':     [1,1,0,1,0],
        'signal_pattern':  [0,1,1,1,1],
        'signal_feeder':   [1,0,0,1,1],
        'signal_count':    [3,2,2,4,3],
        'risk_level':      ['High','Medium','Medium','High','High'],
        'explanation': [
            'WHY: consumption deviates from baseline + feeder-meter energy imbalance\nHOW SERIOUS: High risk (3 signals)\nWHAT TO DO: Immediate physical inspection recommended',
            'WHY: usage is far below peer cluster + unusual evening dip detected\nHOW SERIOUS: Medium risk (2 signals)\nWHAT TO DO: Schedule inspection within 48 hours',
            'WHY: consumption deviates from baseline + unusual evening dip detected\nHOW SERIOUS: Medium risk (2 signals)\nWHAT TO DO: Schedule inspection within 48 hours',
            'WHY: all 4 signals triggered\nHOW SERIOUS: High risk (4 signals)\nWHAT TO DO: Immediate physical inspection recommended',
            'WHY: consumption deviates + evening dip + feeder imbalance\nHOW SERIOUS: High risk (3 signals)\nWHAT TO DO: Immediate physical inspection recommended',
        ]
    })


def load_forecast():
    path = "data/forecast_output.csv"
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=['timestamp'])
    timestamps = pd.date_range('2026-04-01', periods=72, freq='h')
    zones = ['Zone_1','Zone_2','Zone_3','Zone_4','Zone_5']
    records = []
    for zone in zones:
        base = np.random.uniform(80, 140)
        for ts in timestamps:
            peak = 1.4 if 18 <= ts.hour <= 22 else 0.7 if ts.hour <= 5 else 1.0
            records.append({
                'feeder_zone':   zone,
                'timestamp':     ts,
                'total_kwh':     round(base * peak + np.random.normal(0, 3), 2),
                'predicted_kwh': round(base * peak + np.random.normal(0, 2), 2),
            })
    return pd.DataFrame(records)


# ─────────────────────────────────────────────
# PAGE 1 — OPERATOR DASHBOARD
# ─────────────────────────────────────────────
def show_operator_dashboard():
    st.markdown("""
    <div class='amp-header'>
        <div style='font-size:2.6rem; line-height:1;'>⚡</div>
        <div>
            <p class='amp-title'>AMPLYTICS</p>
            <p class='amp-subtitle'>Smart Meter Intelligence Platform — Operator Dashboard</p>
            <span class='amp-badge'>BESCOM · AI FOR BHARAT 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df     = load_alerts()
    total  = len(df)
    high   = len(df[df['risk_level'] == 'High'])
    medium = len(df[df['risk_level'] == 'Medium'])
    low    = len(df[df['risk_level'] == 'Low'])

    # KPI cards — all dark, consistent
    st.markdown(f"""
    <div class='kpi-row'>
        <div class='kpi-card blue'>
            <div class='kpi-label'>Total Alerts</div>
            <div class='kpi-value'>{total}</div>
        </div>
        <div class='kpi-card coral'>
            <div class='kpi-label'>High Risk</div>
            <div class='kpi-value'>{high}</div>
        </div>
        <div class='kpi-card amber'>
            <div class='kpi-label'>Medium Risk</div>
            <div class='kpi-value'>{medium}</div>
        </div>
        <div class='kpi-card teal'>
            <div class='kpi-label'>Low Risk</div>
            <div class='kpi-value'>{low}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("<div class='section-title'>Zone Risk Overview</div>", unsafe_allow_html=True)
        zone_summary = df.groupby(['feeder_zone','risk_level']).size().reset_index(name='count')
        fig = px.bar(
            zone_summary, x='feeder_zone', y='count', color='risk_level', barmode='stack',
            color_discrete_map={'High':'#f85149','Medium':'#d29922','Low':'#3fb950'},
            labels={'feeder_zone':'Feeder Zone','count':'Alert Count','risk_level':'Risk Level'},
        )
        fig.update_layout(**PLOT_BASE, **dark_axes('Feeder Zone','Alert Count'), height=270)
        fig.update_xaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("<div class='section-title'>Signal Breakdown</div>", unsafe_allow_html=True)
        signal_totals = {
            'Residual Deviation': int(df['signal_residual'].sum()),
            'Peer Cluster':       int(df['signal_peer'].sum()),
            'Pattern Flag':       int(df['signal_pattern'].sum()),
            'Feeder Imbalance':   int(df['signal_feeder'].sum()),
        }
        # Single blue family — four tones (fixes the multi-color mess)
        blue_family = ['#1f6feb','#388bfd','#58a6ff','#79c0ff']
        fig2 = go.Figure(go.Bar(
            x=list(signal_totals.values()),
            y=list(signal_totals.keys()),
            orientation='h',
            marker=dict(color=blue_family, line=dict(width=0)),
            text=list(signal_totals.values()),
            textposition='auto',
            textfont=dict(color='#e6edf3', family='Space Mono, monospace', size=12),
        ))
        ax2 = dict(
            xaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d',
                       tickfont=dict(color='#8b949e')),
            yaxis=dict(showgrid=False, linecolor='#30363d',
                       tickfont=dict(color='#c9d1d9', size=11)),
        )
        fig2.update_layout(**PLOT_BASE, **ax2, height=270)
        st.plotly_chart(fig2, use_container_width=True)

    # Alert Queue
    st.markdown("<div class='section-title'>Inspection Alert Queue</div>", unsafe_allow_html=True)

    f1, f2, _ = st.columns([1,1,3])
    with f1:
        filter_risk = st.selectbox("Risk Level", ["All","High","Medium","Low"])
    with f2:
        filter_zone = st.selectbox("Feeder Zone", ["All"] + sorted(df['feeder_zone'].unique().tolist()))

    filtered = df.copy()
    if filter_risk != "All":
        filtered = filtered[filtered['risk_level'] == filter_risk]
    if filter_zone != "All":
        filtered = filtered[filtered['feeder_zone'] == filter_zone]
    filtered = filtered.sort_values('signal_count', ascending=False)

    if filtered.empty:
        st.markdown("<p style='color:#8b949e; padding:20px 0;'>No alerts match the selected filters.</p>",
                    unsafe_allow_html=True)
    else:
        for _, row in filtered.iterrows():
            icon      = {'High':'🔴','Medium':'🟡','Low':'🟢'}.get(row['risk_level'],'⚪')
            lines     = row['explanation'].split('\n')
            why_text  = next((l.replace('WHY: ','') for l in lines if l.startswith('WHY')), '')
            how_text  = next((l.replace('HOW SERIOUS: ','') for l in lines if l.startswith('HOW')), '')
            what_text = next((l.replace('WHAT TO DO: ','') for l in lines if l.startswith('WHAT')), '')

            st.markdown(f"""
            <div class='alert-card {row["risk_level"].lower()}'>
                <div style='display:flex; align-items:center; justify-content:space-between;
                            flex-wrap:wrap; gap:8px;'>
                    <span>
                        <span class='alert-meter'>{icon} {row['meter_id']}</span>
                        <span class='risk-badge {row["risk_level"]}'>{row['risk_level']} Risk</span>
                    </span>
                    <span class='alert-meta'>
                        Zone: {row['feeder_zone']} &nbsp;·&nbsp; {row['signal_count']} signals triggered
                    </span>
                </div>
                <div class='why-block'>
                    <span class='why-key'>WHY ›</span> {why_text}<br>
                    <span class='why-key'>HOW SERIOUS ›</span> {how_text}<br>
                    <span class='why-key'>WHAT TO DO ›</span> {what_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("View Raw Alert Table"):
        st.dataframe(df, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE 2 — CONSUMER DASHBOARD
# ─────────────────────────────────────────────
def show_consumer_dashboard():
    st.markdown("""
    <div class='amp-header'>
        <div style='font-size:2.6rem; line-height:1;'>💡</div>
        <div>
            <p class='amp-title'>MY ELECTRICITY</p>
            <p class='amp-subtitle'>Consumer Transparency Module — Real-time Usage &amp; Bill Prediction</p>
            <span class='amp-badge'>POWERED BY AMPLYTICS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    forecast = load_forecast()

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        feeder_zone = st.selectbox("Select Your Feeder Zone",
                                   sorted(forecast['feeder_zone'].unique()))
    with col_s2:
        meter_id = st.selectbox("Select Your Meter ID",
            ['MTR_0005','MTR_0010','MTR_0015','MTR_0020','MTR_0025','MTR_0030'])

    zone_data = forecast[forecast['feeder_zone'] == feeder_zone].copy()

    # Bill calculation — divide by meters_per_zone to get realistic per-consumer figure
    rate_per_kwh    = 6.5
    total_actual    = zone_data['total_kwh'].sum()
    days_in_data    = max(1, (zone_data['timestamp'].max() - zone_data['timestamp'].min()).days + 1)
    meters_per_zone = 200
    projected_kwh   = (total_actual / days_in_data) * 30 / meters_per_zone
    projected_bill  = projected_kwh * rate_per_kwh

    st.markdown("<br>", unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(f"""
        <div class='bill-card'>
            <div class='kpi-label' style='text-align:center;'>Predicted Month-End Bill</div>
            <div class='bill-amount'>Rs.{projected_bill:,.0f}</div>
            <div class='bill-sublabel'>Based on current usage trajectory</div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown(f"""
        <div class='kpi-card blue' style='height:100%; box-sizing:border-box;'>
            <div class='kpi-label'>Projected Usage</div>
            <div class='kpi-value'>{projected_kwh:,.0f}</div>
            <div style='color:#8b949e; font-size:0.78rem; margin-top:6px;'>kWh this month</div>
        </div>
        """, unsafe_allow_html=True)
    with b3:
        st.markdown(f"""
        <div class='kpi-card amber' style='height:100%; box-sizing:border-box;'>
            <div class='kpi-label'>Rate Applied</div>
            <div class='kpi-value'>Rs.{rate_per_kwh}</div>
            <div style='color:#8b949e; font-size:0.78rem; margin-top:6px;'>per kWh (BESCOM tariff)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Hourly consumption chart
    st.markdown("<div class='section-title'>Your Hourly Consumption</div>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=zone_data['timestamp'], y=zone_data['total_kwh'],
        name='Actual Usage',
        line=dict(color='#58a6ff', width=2),
        fill='tozeroy', fillcolor='rgba(88,166,255,0.07)'
    ))
    fig.add_trace(go.Scatter(
        x=zone_data['timestamp'], y=zone_data['predicted_kwh'],
        name='AI Forecast',
        line=dict(color='#f0c040', width=2, dash='dot'),
    ))
    ax_line = dict(
        xaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d',
                   tickfont=dict(color='#8b949e'), title='Date / Hour',
                   title_font=dict(color='#8b949e')),
        yaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d',
                   tickfont=dict(color='#8b949e'), title='Consumption (kWh)',
                   title_font=dict(color='#8b949e')),
    )
    fig.update_layout(**PLOT_BASE, **ax_line, height=310, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # Peak hours chart
    st.markdown("<div class='section-title'>Average Usage by Hour of Day</div>", unsafe_allow_html=True)

    zone_data['hour'] = zone_data['timestamp'].dt.hour
    hourly_avg = zone_data.groupby('hour')['total_kwh'].mean().reset_index()
    hourly_avg['is_peak'] = hourly_avg['hour'].between(18, 22)

    # Vibrant blue for normal, coral for peak
    bar_colors = ['#f85149' if p else '#388bfd' for p in hourly_avg['is_peak']]

    fig3 = go.Figure(go.Bar(
        x=hourly_avg['hour'],
        y=hourly_avg['total_kwh'],
        marker=dict(color=bar_colors, line=dict(width=0)),
        hovertemplate='Hour %{x}:00 &mdash; %{y:.1f} kWh<extra></extra>',
    ))
    ax_bar = dict(
        xaxis=dict(showgrid=False, linecolor='#30363d', dtick=1,
                   tickfont=dict(color='#8b949e'), title='Hour of Day',
                   title_font=dict(color='#8b949e')),
        yaxis=dict(showgrid=True, gridcolor='#21262d', linecolor='#30363d',
                   tickfont=dict(color='#8b949e'), title='Avg kWh',
                   title_font=dict(color='#8b949e')),
    )
    fig3.update_layout(**PLOT_BASE, **ax_bar, height=250)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        "<p style='color:#8b949e; font-size:0.82rem; margin-top:-8px;'>"
        "Coral bars = peak hours (6 PM - 10 PM). Shifting heavy appliances outside these hours "
        "reduces your bill and helps BESCOM manage grid load.</p>",
        unsafe_allow_html=True
    )

    # Tip box
    st.markdown(f"""
    <div style='background:#161b22; border:1px solid #21262d; border-left:4px solid #f0c040;
                border-radius:8px; padding:14px 18px; margin-top:12px;
                font-size:0.88rem; color:#c9d1d9; line-height:1.7;'>
        <span style='font-family:Space Mono,monospace; color:#f0c040;
                     font-size:0.72rem; letter-spacing:1px;'>TIP</span><br>
        Meter <b style='color:#e6edf3;'>{meter_id}</b> — estimated bill for
        <b style='color:#e6edf3;'>{feeder_zone}</b> this month is
        <b style='color:#f0c040;'>Rs. {projected_bill:,.0f}</b>.
        Peak usage is between 6 PM and 10 PM. Shifting heavy appliances outside
        these hours can lower your bill and support the grid.
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View Raw Forecast Data"):
        st.dataframe(zone_data.drop(columns=['hour']), use_container_width=True)


# ─────────────────────────────────────────────
# ROUTING
# ─────────────────────────────────────────────
if "Operator" in page:
    show_operator_dashboard()
else:
    show_consumer_dashboard()