import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error


def build_features(df):
    df = df.sort_values(['feeder_zone', 'timestamp'])

    feeder_hourly = df.groupby(['feeder_zone', 'timestamp'])['consumption_kwh'].sum().reset_index()
    feeder_hourly.columns = ['feeder_zone', 'timestamp', 'total_kwh']

    feeder_hourly['hour'] = pd.to_datetime(feeder_hourly['timestamp']).dt.hour
    feeder_hourly['day_of_week'] = pd.to_datetime(feeder_hourly['timestamp']).dt.dayofweek
    feeder_hourly['is_weekend'] = (feeder_hourly['day_of_week'] >= 5).astype(int)
    feeder_hourly['day_of_month'] = pd.to_datetime(feeder_hourly['timestamp']).dt.day

    feeder_hourly = feeder_hourly.sort_values(['feeder_zone', 'timestamp'])
    grp = feeder_hourly.groupby('feeder_zone')['total_kwh']
    feeder_hourly['lag_1h'] = grp.shift(1)
    feeder_hourly['lag_24h'] = grp.shift(24)
    feeder_hourly['lag_168h'] = grp.shift(168)

    feeder_hourly = feeder_hourly.dropna()
    return feeder_hourly


def train_and_forecast(df):
    feature_df = build_features(df)

    feature_cols = ['hour', 'day_of_week', 'is_weekend',
                    'day_of_month', 'lag_1h', 'lag_24h', 'lag_168h']
    target = 'total_kwh'

    results = []
    for zone in feature_df['feeder_zone'].unique():
        zone_df = feature_df[feature_df['feeder_zone'] == zone].copy()

        split = int(len(zone_df) * 0.9)
        train = zone_df.iloc[:split]
        test = zone_df.iloc[split:]

        model = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1)
        model.fit(train[feature_cols], train[target])

        test = test.copy()
        test['predicted_kwh'] = model.predict(test[feature_cols])

        mae = mean_absolute_error(test[target], test['predicted_kwh'])
        mape = (abs(test[target] - test['predicted_kwh']) / test[target]).mean() * 100
        print(f'{zone} — MAE: {mae:.2f}, MAPE: {mape:.1f}%')

        results.append(test[['feeder_zone', 'timestamp', target, 'predicted_kwh']])

    output = pd.concat(results)
    output.to_csv('data/forecast_output.csv', index=False)
    print('Done! forecast_output.csv saved.')
    return output


if __name__ == '__main__':
    df = pd.read_csv('data/clean_meter_data.csv', parse_dates=['timestamp'])
    train_and_forecast(df)