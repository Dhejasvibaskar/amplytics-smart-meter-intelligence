import pandas as pd
import numpy as np
from alert_fusion import fuse_alerts
from decision_support import build_decision_output

def generate_severity_trend(anomaly_df):
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    
    records = []
    for date in dates:
        # Slightly vary signal counts each day to simulate real monitoring
        daily_df = anomaly_df.copy()
        noise = np.random.randint(0, 2, size=len(daily_df))
        daily_df['signal_residual'] = (daily_df['signal_residual'] + noise) % 2
        
        fused = fuse_alerts(daily_df)
        counts = fused['risk_level'].value_counts()
        
        records.append({
            'date': date.strftime('%Y-%m-%d'),
            'High': counts.get('High', 0),
            'Medium': counts.get('Medium', 0),
            'Low': counts.get('Low', 0),
        })
    
    trend_df = pd.DataFrame(records)
    trend_df.to_csv('../data/severity_trend.csv', index=False)
    print(trend_df.to_string())
    return trend_df

if __name__ == '__main__':
    df = pd.read_csv('../data/anomaly_signals.csv')
    generate_severity_trend(df)