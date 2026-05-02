import pandas as pd
import numpy as np
import os

def generate_data():
    np.random.seed(42)
    n_meters = 50
    n_days = 30

    records = []

    for meter_id in range(1, n_meters + 1):
        feeder_zone = f'Zone_{(meter_id % 5) + 1}'
        base = np.random.uniform(5, 20)

        for day in range(n_days):
            for hour in range(24):
                tod_factor = 1.5 if 18 <= hour <= 22 else 0.7 if 0 <= hour <= 5 else 1.0
                consumption = base * tod_factor + np.random.normal(0, 0.5)

                # Inject theft
                if meter_id % 5 == 0 and day > 15:
                    consumption *= 0.15

                records.append({
                    'meter_id': f'MTR_{meter_id:04d}',
                    'feeder_zone': feeder_zone,
                    'timestamp': pd.Timestamp('2026-04-01') + pd.Timedelta(days=day, hours=hour),
                    'consumption_kwh': max(0, round(consumption, 3))
                })

    df = pd.DataFrame(records)

    # 🔥 CREATE FOLDER IF NOT EXISTS
    os.makedirs('data', exist_ok=True)

    df.to_csv('data/smart_meter_data.csv', index=False)
    print("✅ Data generated:", len(df))


if __name__ == "__main__":
    generate_data()