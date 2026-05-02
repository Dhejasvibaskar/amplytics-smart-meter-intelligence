import pandas as pd
from alert_fusion import fuse_alerts

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

def build_decision_output(fused_df):
    fused_df['explanation'] = fused_df.apply(generate_explanation, axis=1)
    return fused_df

if __name__ == '__main__':
    df = pd.read_csv('../data/anomaly_signals.csv')
    fused = fuse_alerts(df)
    final = build_decision_output(fused)
    final.to_csv('../data/alerts_with_explanations.csv', index=False)
    print(final[['meter_id', 'risk_level', 'explanation']].to_string())