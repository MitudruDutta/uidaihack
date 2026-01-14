import pandas as pd
import numpy as np

print("=" * 70)
print("DEEP BRUTAL AUDIT - ANALYTICS DATASETS")
print("=" * 70)

enrol = pd.read_csv('data/analytics/enrolment_agg.csv')
bio = pd.read_csv('data/analytics/biometric_agg.csv')
demo = pd.read_csv('data/analytics/demographic_agg.csv')

enrol['date'] = pd.to_datetime(enrol['date'])
bio['date'] = pd.to_datetime(bio['date'])
demo['date'] = pd.to_datetime(demo['date'])

# 1. DATE GAPS ANALYSIS
print("\n" + "#" * 70)
print("# 1. DATE GAPS - WHERE IS DATA MISSING?")
print("#" * 70)

for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
    all_dates = pd.date_range(df['date'].min(), df['date'].max())
    present_dates = set(df['date'].unique())
    missing_dates = [d for d in all_dates if d not in present_dates]
    print(f"\n{name}:")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  Expected days: {len(all_dates)}, Present: {len(present_dates)}, Missing: {len(missing_dates)}")
    if missing_dates:
        print(f"  Missing dates sample: {[str(d.date()) for d in missing_dates[:10]]}")

# 2. STATE-WISE DATA COMPLETENESS
print("\n" + "#" * 70)
print("# 2. STATE-WISE COMPLETENESS - WHO HAS GAPS?")
print("#" * 70)

for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
    print(f"\n{name}:")
    state_dates = df.groupby('state')['date'].nunique()
    max_dates = df['date'].nunique()
    incomplete = state_dates[state_dates < max_dates * 0.8]  # Less than 80% coverage
    if len(incomplete) > 0:
        print(f"  States with <80% date coverage:")
        for s, d in incomplete.sort_values().head(10).items():
            print(f"    {s}: {d}/{max_dates} days ({d / max_dates * 100:.0f}%)")
    else:
        print(f"  All states have >80% date coverage")

# 3. OUTLIER DETECTION - EXTREME VALUES
print("\n" + "#" * 70)
print("# 3. OUTLIERS - SUSPICIOUSLY HIGH VALUES")
print("#" * 70)

for name, df, cols in [
    ('ENROLMENT', enrol, ['age_0_5', 'age_5_17', 'age_18_greater', 'total']),
    ('BIOMETRIC', bio, ['bio_age_5_17', 'bio_age_17_', 'total']),
    ('DEMOGRAPHIC', demo, ['demo_age_5_17', 'demo_age_17_', 'total'])
]:
    print(f"\n{name}:")
    for col in cols:
        q99 = df[col].quantile(0.99)
        q999 = df[col].quantile(0.999)
        max_val = df[col].max()
        extreme = df[df[col] > q999]
        print(f"  {col}: 99%={q99:.0f}, 99.9%={q999:.0f}, max={max_val}")
        if len(extreme) > 0:
            print(f"    Extreme rows (>{q999:.0f}): {len(extreme)}")
            top = df.nlargest(3, col)[['date', 'state', 'district', 'pincode', col]]
            for _, row in top.iterrows():
                print(
                    f"      {row['date'].date()} | {row['state'][:15]} | {row['district'][:15]} | {row['pincode']} | {row[col]}")

# 4. ZERO ANALYSIS - WHERE IS NOTHING HAPPENING?
print("\n" + "#" * 70)
print("# 4. ZERO ANALYSIS - DEAD ZONES")
print("#" * 70)

for name, df, cols in [
    ('ENROLMENT', enrol, ['age_0_5', 'age_5_17', 'age_18_greater']),
    ('BIOMETRIC', bio, ['bio_age_5_17', 'bio_age_17_']),
    ('DEMOGRAPHIC', demo, ['demo_age_5_17', 'demo_age_17_'])
]:
    print(f"\n{name}:")
    for col in cols:
        zeros = (df[col] == 0).sum()
        pct = zeros / len(df) * 100
        print(f"  {col}: {zeros:,} zeros ({pct:.1f}%)")

    # States with most zeros
    df['_zeros'] = (df[cols] == 0).sum(axis=1)
    all_zero = (df['_zeros'] == len(cols)).sum()
    print(f"  Rows with ALL zeros: {all_zero}")

# 5. PINCODE-DISTRICT CONSISTENCY
print("\n" + "#" * 70)
print("# 5. PINCODE-DISTRICT MAPPING CHAOS")
print("#" * 70)

for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
    pin_dist = df.groupby('pincode')['district'].nunique()
    multi = pin_dist[pin_dist > 1]
    print(f"\n{name}:")
    print(f"  Pincodes mapping to multiple districts: {len(multi)}")
    if len(multi) > 0:
        worst = multi.nlargest(5)
        for pin, count in worst.items():
            districts = df[df['pincode'] == pin]['district'].unique()
            print(f"    {pin}: {count} districts -> {list(districts)[:3]}")

# 6. STATE-DISTRICT COUNT VALIDATION
print("\n" + "#" * 70)
print("# 6. STATE-DISTRICT COUNTS - DOES IT MATCH REALITY?")
print("#" * 70)

# Expected district counts (approximate)
EXPECTED_DISTRICTS = {
    'Uttar Pradesh': 75, 'Madhya Pradesh': 55, 'Bihar': 38, 'Maharashtra': 36,
    'Rajasthan': 50, 'Tamil Nadu': 38, 'Karnataka': 31, 'Gujarat': 33,
    'Andhra Pradesh': 26, 'Telangana': 33, 'West Bengal': 23, 'Odisha': 30,
    'Kerala': 14, 'Assam': 35, 'Punjab': 23, 'Haryana': 22,
}

for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
    print(f"\n{name}:")
    state_dist = df.groupby('state')['district'].nunique()
    for state, expected in EXPECTED_DISTRICTS.items():
        if state in state_dist.index:
            actual = state_dist[state]
            diff = actual - expected
            if abs(diff) > 5:
                print(f"  {state}: {actual} (expected ~{expected}, diff={diff:+d})")

# 7. DAILY VOLUME ANOMALIES
print("\n" + "#" * 70)
print("# 7. DAILY VOLUME ANOMALIES")
print("#" * 70)

for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
    daily = df.groupby('date')['total'].sum()
    mean_daily = daily.mean()
    std_daily = daily.std()

    low_days = daily[daily < mean_daily - 2 * std_daily]
    high_days = daily[daily > mean_daily + 2 * std_daily]

    print(f"\n{name}:")
    print(f"  Daily mean: {mean_daily:,.0f}, std: {std_daily:,.0f}")
    print(f"  Anomaly low days (<mean-2std): {len(low_days)}")
    if len(low_days) > 0:
        for d, v in low_days.nsmallest(3).items():
            print(f"    {d.date()}: {v:,}")
    print(f"  Anomaly high days (>mean+2std): {len(high_days)}")
    if len(high_days) > 0:
        for d, v in high_days.nlargest(3).items():
            print(f"    {d.date()}: {v:,}")

# 8. AGE GROUP RATIO SANITY
print("\n" + "#" * 70)
print("# 8. AGE GROUP RATIOS - DO THEY MAKE SENSE?")
print("#" * 70)

# Enrolment
e_0_5 = enrol['age_0_5'].sum()
e_5_17 = enrol['age_5_17'].sum()
e_18 = enrol['age_18_greater'].sum()
e_total = e_0_5 + e_5_17 + e_18
print(f"\nENROLMENT age distribution:")
print(f"  0-5 years: {e_0_5:,} ({e_0_5 / e_total * 100:.1f}%)")
print(f"  5-17 years: {e_5_17:,} ({e_5_17 / e_total * 100:.1f}%)")
print(f"  18+ years: {e_18:,} ({e_18 / e_total * 100:.1f}%)")
print(f"  CONCERN: 18+ is only {e_18 / e_total * 100:.1f}% - are adults not enrolling?")

# Biometric
b_5_17 = bio['bio_age_5_17'].sum()
b_17 = bio['bio_age_17_'].sum()
b_total = b_5_17 + b_17
print(f"\nBIOMETRIC age distribution:")
print(f"  5-17 years: {b_5_17:,} ({b_5_17 / b_total * 100:.1f}%)")
print(f"  17+ years: {b_17:,} ({b_17 / b_total * 100:.1f}%)")

# Demographic
d_5_17 = demo['demo_age_5_17'].sum()
d_17 = demo['demo_age_17_'].sum()
d_total = d_5_17 + d_17
print(f"\nDEMOGRAPHIC age distribution:")
print(f"  5-17 years: {d_5_17:,} ({d_5_17 / d_total * 100:.1f}%)")
print(f"  17+ years: {d_17:,} ({d_17 / d_total * 100:.1f}%)")

# 9. CROSS-DATASET CONSISTENCY
print("\n" + "#" * 70)
print("# 9. CROSS-DATASET CONSISTENCY")
print("#" * 70)

# Same pincode should have similar activity patterns
common_pins = set(enrol['pincode']) & set(bio['pincode']) & set(demo['pincode'])
print(f"\nCommon pincodes: {len(common_pins)}")

# Check if high-enrolment pincodes also have high updates
e_by_pin = enrol.groupby('pincode')['total'].sum()
b_by_pin = bio.groupby('pincode')['total'].sum()
d_by_pin = demo.groupby('pincode')['total'].sum()

# Correlation
common_list = list(common_pins)
e_vals = e_by_pin.reindex(common_list).fillna(0)
b_vals = b_by_pin.reindex(common_list).fillna(0)
d_vals = d_by_pin.reindex(common_list).fillna(0)

corr_eb = np.corrcoef(e_vals, b_vals)[0, 1]
corr_ed = np.corrcoef(e_vals, d_vals)[0, 1]
corr_bd = np.corrcoef(b_vals, d_vals)[0, 1]

print(f"\nPincode-level correlations:")
print(f"  Enrolment vs Biometric: {corr_eb:.3f}")
print(f"  Enrolment vs Demographic: {corr_ed:.3f}")
print(f"  Biometric vs Demographic: {corr_bd:.3f}")

# 10. WEEKEND/WEEKDAY PATTERN
print("\n" + "#" * 70)
print("# 10. WEEKEND vs WEEKDAY PATTERN")
print("#" * 70)

for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
    df['_dow'] = df['date'].dt.dayofweek
    weekday = df[df['_dow'] < 5]['total'].sum()
    weekend = df[df['_dow'] >= 5]['total'].sum()

    weekday_days = df[df['_dow'] < 5]['date'].nunique()
    weekend_days = df[df['_dow'] >= 5]['date'].nunique()

    weekday_avg = weekday / weekday_days if weekday_days > 0 else 0
    weekend_avg = weekend / weekend_days if weekend_days > 0 else 0

    print(f"\n{name}:")
    print(f"  Weekday avg: {weekday_avg:,.0f}/day")
    print(f"  Weekend avg: {weekend_avg:,.0f}/day")
    print(f"  Weekend/Weekday ratio: {weekend_avg / weekday_avg:.2f}" if weekday_avg > 0 else "  N/A")

print("\n" + "=" * 70)
print("DEEP AUDIT COMPLETE")
print("=" * 70)
