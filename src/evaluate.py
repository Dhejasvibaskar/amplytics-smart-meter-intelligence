import pandas as pd

# Load your outputs
signals = pd.read_csv('data/anomaly_signals.csv')

# These are the meters where theft was injected
# meter_id number divisible by 5
theft_meters = ['MTR_0005', 'MTR_0010', 'MTR_0015', 'MTR_0020', 'MTR_0025',
                'MTR_0030', 'MTR_0035', 'MTR_0040', 'MTR_0045', 'MTR_0050']

normal_meters = [m for m in signals['meter_id'] if m not in theft_meters]

# A meter is "detected" if 2 or more signals fire (same rule as Layer 3)
signals['signal_count'] = (
    signals['signal_residual'] +
    signals['signal_peer'] +
    signals['signal_pattern'] +
    signals['signal_feeder']
)
signals['detected'] = (signals['signal_count'] >= 2).astype(int)

# Actual labels — 1 = theft, 0 = normal
signals['actual'] = signals['meter_id'].isin(theft_meters).astype(int)

# Calculate metrics
TP = len(signals[(signals['actual'] == 1) & (signals['detected'] == 1)])
FP = len(signals[(signals['actual'] == 0) & (signals['detected'] == 1)])
TN = len(signals[(signals['actual'] == 0) & (signals['detected'] == 0)])
FN = len(signals[(signals['actual'] == 1) & (signals['detected'] == 0)])

precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall    = TP / (TP + FN) if (TP + FN) > 0 else 0
fpr       = FP / (FP + TN) if (FP + TN) > 0 else 0

print("=" * 40)
print("   AMPLYTICS — DETECTION METRICS")
print("=" * 40)
print(f"  Theft meters injected     : {len(theft_meters)}")
print(f"  Theft meters caught (TP)  : {TP}")
print(f"  Missed (FN)               : {FN}")
print(f"  False alarms (FP)         : {FP}")
print("-" * 40)
print(f"  Precision                 : {precision*100:.1f}%")
print(f"  Recall                    : {recall*100:.1f}%")
print(f"  False Positive Rate       : {fpr*100:.1f}%")
print("=" * 40)

# Show which theft meters were caught and which were missed
print("\n  THEFT METER BREAKDOWN:")
print("-" * 40)
for _, row in signals[signals['actual'] == 1].iterrows():
    status = "✅ CAUGHT" if row['detected'] else "❌ MISSED"
    print(f"  {row['meter_id']} — {status} ({int(row['signal_count'])} signals)")