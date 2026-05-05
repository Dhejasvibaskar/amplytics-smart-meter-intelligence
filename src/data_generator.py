import pandas as pd
import numpy as np
import os


def generate_data():
    np.random.seed(42)

    n_meters = 50
    n_days = 30

    # Zone mapping based on your dashboard
    zone_area_map = {
        "Zone_1": "Rajajinagar",
        "Zone_2": "Koramangala",
        "Zone_3": "Hebbal",
        "Zone_4": "BTM Layout",
        "Zone_5": "Indiranagar",
    }

    # Realistic Bangalore monthly usage targets
    # These are per-household ranges in kWh/month
    zone_monthly_usage = {
        "Zone_1": (180, 280),  # Rajajinagar
        "Zone_2": (160, 260),  # Koramangala
        "Zone_3": (140, 230),  # Hebbal
        "Zone_4": (190, 300),  # BTM Layout
        "Zone_5": (220, 350),  # Indiranagar
    }
    

    records = []

    for meter_id in range(1, n_meters + 1):
        feeder_zone = f"Zone_{((meter_id - 1) % 5) + 1}"
        area_name = zone_area_map[feeder_zone]

        monthly_target = np.random.uniform(*zone_monthly_usage[feeder_zone])
        daily_target = monthly_target / n_days

        for day in range(n_days):
            is_weekend = day % 7 in [5, 6]

            for hour in range(24):
                # Bangalore-style household pattern
                if 6 <= hour <= 9:
                    tod_factor = 1.25  # morning geyser/cooking usage
                elif 18 <= hour <= 22:
                    tod_factor = 1.45  # evening peak usage
                elif 0 <= hour <= 5:
                    tod_factor = 0.45  # night low usage
                else:
                    tod_factor = 0.85  # normal daytime usage

                weekend_factor = 1.08 if is_weekend else 1.0

                # Normalize so daily consumption stays close to target
                base_hourly = daily_target / 24
                consumption = base_hourly * tod_factor * weekend_factor

                # Small realistic noise
                consumption += np.random.normal(0, base_hourly * 0.15)

                # Inject theft/loss pattern after day 15
                # One meter per zone is suspicious: MTR_0005, 0010, 0015...
                if meter_id % 5 == 0 and day > 15:
                    consumption *= 0.25

                records.append({
                    "meter_id": f"MTR_{meter_id:04d}",
                    "feeder_zone": feeder_zone,
                    "area_name": area_name,
                    "timestamp": pd.Timestamp("2026-04-01") + pd.Timedelta(days=day, hours=hour),
                    "consumption_kwh": max(0, round(consumption, 3)),
                })

    df = pd.DataFrame(records)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/smart_meter_data.csv", index=False)

    print("Data generated:", len(df))
    print("Saved to data/smart_meter_data.csv")
    print("\nMonthly usage by zone:")
    print(df.groupby("feeder_zone")["consumption_kwh"].sum().round(2))


if __name__ == "__main__":
    generate_data()