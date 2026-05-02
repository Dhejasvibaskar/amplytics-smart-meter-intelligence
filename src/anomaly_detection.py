import pandas as pd
import numpy as np
import os

def signal_residual_deviation(df):
    df['residual'] = df['consumption_kwh'] - df['rolling_avg_24h']
    stats = df.groupby('meter_id')['residual'].agg(['mean', 'std']).reset_index()
    stats['signal_residual'] = (stats['std'] > stats['std'].quantile(0.85)).astype(int)
    return stats[['meter_id', 'signal_residual']]


def signal_peer_cluster(df):
    peer = df.groupby(['feeder_zone', 'meter_id'])['consumption_kwh'].mean().reset_index()
    zone_avg = peer.groupby('feeder_zone')['consumption_kwh'].mean().reset_index()
    zone_avg.columns = ['feeder_zone', 'zone_avg']

    peer = peer.merge(zone_avg, on='feeder_zone')
    peer['signal_peer'] = (peer['consumption_kwh'] < peer['zone_avg'] * 0.5).astype(int)

    return peer[['meter_id', 'signal_peer']]


def signal_pattern_flag(df):
    evening = df[df['hour'].between(18, 22)]
    eve_avg = evening.groupby('meter_id')['consumption_kwh'].mean().reset_index()

    threshold = eve_avg['consumption_kwh'].quantile(0.15)
    eve_avg['signal_pattern'] = (eve_avg['consumption_kwh'] < threshold).astype(int)

    return eve_avg[['meter_id', 'signal_pattern']]


def signal_feeder_imbalance(df):
    meter_sum = df.groupby('feeder_zone')['consumption_kwh'].sum().reset_index()
    meter_sum.columns = ['feeder_zone', 'meter_total']

    np.random.seed(0)
    meter_sum['feeder_reading'] = meter_sum['meter_total'] * np.random.uniform(0.7, 1.0, len(meter_sum))

    meter_sum['imbalance_pct'] = abs(meter_sum['meter_total'] - meter_sum['feeder_reading']) / meter_sum['feeder_reading']

    bad_zones = meter_sum[meter_sum['imbalance_pct'] > 0.15]['feeder_zone'].tolist()

    meters = df[['meter_id', 'feeder_zone']].drop_duplicates()
    meters['signal_feeder'] = meters['feeder_zone'].isin(bad_zones).astype(int)

    return meters[['meter_id', 'signal_feeder']]


def run_all_signals(df):
    s1 = signal_residual_deviation(df)
    s2 = signal_peer_cluster(df)
    s3 = signal_pattern_flag(df)
    s4 = signal_feeder_imbalance(df)

    result = s1.merge(s2, on='meter_id') \
               .merge(s3, on='meter_id') \
               .merge(s4, on='meter_id')

    feeder_map = df[['meter_id', 'feeder_zone']].drop_duplicates()
    result = result.merge(feeder_map, on='meter_id')

    os.makedirs('data', exist_ok=True)

    result.to_csv('data/anomaly_signals.csv', index=False)
    print("✅ Anomaly detection done")

    return result


if __name__ == "__main__":
    df = pd.read_csv('data/clean_meter_data.csv', parse_dates=['timestamp'])
    run_all_signals(df)