import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error


def build_features(df):
    df = df.sort_values(['meter_id', 'timestamp'])

    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['day_of_month'] = pd.to_datetime(df['timestamp']).dt.day

    grp = df.groupby('meter_id')['consumption_kwh']
    df['lag_1h'] = grp.shift(1)
    df['lag_24h'] = grp.shift(24)
    df['lag_168h'] = grp.shift(168)

    df = df.dropna()
    return df


def train_and_forecast(df):
    feature_df = build_features(df)

    feature_cols = ['hour', 'day_of_week', 'is_weekend',
                    'day_of_month', 'lag_1h', 'lag_24h', 'lag_168h']
    target = 'consumption_kwh'

    results = []
    meters = feature_df['meter_id'].unique()
    total = len(meters)

    for i, meter in enumerate(meters):
        meter_df = feature_df[feature_df['meter_id'] == meter].copy()

        split = int(len(meter_df) * 0.9)
        train = meter_df.iloc[:split]
        test = meter_df.iloc[split:]

        if len(train) < 10 or len(test) < 1:
            continue

        model = XGBRegressor(n_estimators=100, max_depth=4,
                             learning_rate=0.1, verbosity=0)
        model.fit(train[feature_cols], train[target])

        test = test.copy()
        test['predicted_kwh'] = model.predict(test[feature_cols])

        mae = mean_absolute_error(test[target], test['predicted_kwh'])
        mape = (abs(test[target] - test['predicted_kwh']) /
                test[target]).mean() * 100
        print(f'[{i+1}/{total}] {meter} — MAE: {mae:.2f}, MAPE: {mape:.1f}%')

        results.append(test[['meter_id', 'feeder_zone',
                              'timestamp', target, 'predicted_kwh']])

    output = pd.concat(results)
    output = output.rename(columns={'consumption_kwh': 'total_kwh'})
    # Add meter count per zone for per-meter bill calculation
    meter_count = df.groupby('feeder_zone')['meter_id'].nunique().reset_index()
    meter_count.columns = ['feeder_zone', 'zone_meter_count']
    output = output.merge(meter_count, on='feeder_zone', how='left')
    output['meter_kwh'] = output['total_kwh'] / output['zone_meter_count']
    output['meter_predicted_kwh'] = output['predicted_kwh'] / output['zone_meter_count']        
    output.to_csv('data/forecast_output.csv', index=False)
    print(f'\nDone! forecast_output.csv saved with {len(output)} rows.')
    print('Columns:', output.columns.tolist())
    return output


if __name__ == '__main__':
    df = pd.read_csv('data/clean_meter_data.csv', parse_dates=['timestamp'])
    train_and_forecast(df)