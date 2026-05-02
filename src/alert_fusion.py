def generate_alert(row):
    signals = 0

    if row["residual_score"] > 0.7:
        signals += 1
    if row["peer_deviation"] > 0.5:
        signals += 1
    if row["pattern_flag"]:
        signals += 1
    if row["feeder_imbalance"]:
        signals += 1

    return signals >= 2