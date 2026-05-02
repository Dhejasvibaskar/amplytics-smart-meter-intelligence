import pandas as pd

def fuse_alerts(anomaly_df):
    anomaly_df['signal_count'] = (
        anomaly_df['signal_residual'] +
        anomaly_df['signal_peer'] +
        anomaly_df['signal_pattern'] +
        anomaly_df['signal_feeder']
    )

    anomaly_df['alert_triggered'] = anomaly_df['signal_count'] >= 2

    def classify_risk(count):
        if count >= 3: return 'High'
        elif count == 2: return 'Medium'
        else: return 'Low'

    anomaly_df['risk_level'] = anomaly_df['signal_count'].apply(classify_risk)
    return anomaly_df[anomaly_df['alert_triggered'] == True]

if __name__ == '__main__':
    df = pd.read_csv('../data/anomaly_signals.csv')
    result = fuse_alerts(df)
    print(result[['meter_id', 'risk_level', 'signal_count']])