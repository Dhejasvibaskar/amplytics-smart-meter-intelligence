import pandas as pd
import os

def clean_and_enrich(df):
    df = df.sort_values(['meter_id', 'timestamp'])

    df['consumption_kwh'] = df.groupby('meter_id')['consumption_kwh'] \
        .transform(lambda x: x.ffill().fillna(0))

    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_peak_hour'] = df['hour'].between(18, 22).astype(int)

    df['rolling_avg_24h'] = df.groupby('meter_id')['consumption_kwh'] \
        .transform(lambda x: x.rolling(24, min_periods=1).mean())

    return df


if __name__ == "__main__":
    df = pd.read_csv('data/smart_meter_data.csv', parse_dates=['timestamp'])
    df_clean = clean_and_enrich(df)

    os.makedirs('data', exist_ok=True)

    df_clean.to_csv('data/clean_meter_data.csv', index=False)
    print("✅ Preprocessing done:", len(df_clean))