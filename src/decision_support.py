import pandas as pd
from alert_fusion import fuse_alerts

BESCOM_TARIFF = 6.5  # Rs per kWh

def generate_explanation(row):
    reasons = []

    if row['signal_residual']:
        reasons.append('consumption deviates from baseline')
    if row['signal_peer']:
        reasons.append('usage is far below peer cluster')
    if row['signal_pattern']:
        reasons.append('unusual evening dip pattern detected')
    if row['signal_feeder']:
        reasons.append('feeder-meter energy imbalance')

    severity = row['risk_level']
    if severity == 'High':
        action = 'Immediate physical inspection recommended'
    elif severity == 'Medium':
        action = 'Schedule inspection within 48 hours'
    else:
        action = 'Monitor for 3 days before action'

    why = 'WHY: ' + ' + '.join(reasons)
    how = f'HOW SERIOUS: {severity} risk ({row["signal_count"]} signals)'
    what = 'WHAT TO DO: ' + action
    return f'{why}\n{how}\n{what}'

def calculate_revenue_loss(row):
    avg_deviation = row['signal_count'] * 0.15
    estimated_kwh_loss = avg_deviation * 5* 24 * 30
    revenue_loss = estimated_kwh_loss * BESCOM_TARIFF
    return round(revenue_loss, 2)

def calculate_confidence(row):
    confidence = (row['signal_count'] / 4) * 100
    return round(confidence, 1)

def build_decision_output(fused_df):
    fused_df['explanation'] = fused_df.apply(generate_explanation, axis=1)
    fused_df['confidence_pct'] = fused_df.apply(calculate_confidence, axis=1)
    fused_df['estimated_monthly_loss_inr'] = fused_df.apply(calculate_revenue_loss, axis=1)
    fused_df['loss_display'] = fused_df['estimated_monthly_loss_inr'].apply(
        lambda x: f'Rs {x:,.0f}/month'
    )
    return fused_df

if __name__ == '__main__':
    df = pd.read_csv('../data/anomaly_signals.csv')
    fused = fuse_alerts(df)
    final = build_decision_output(fused)
    final.to_csv('../data/alerts_with_explanations.csv', index=False)
    print(final[['meter_id', 'risk_level', 'confidence_pct', 'loss_display']].to_string())