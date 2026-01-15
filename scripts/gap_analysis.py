"""
UIDAI Hackathon - Brutal Data Gap Analysis
Deep dive into missing data by state, district, pincode
"""

import pandas as pd
import numpy as np


def load_data():
    enrol = pd.read_csv('data/analytics/enrolment_agg.csv')
    bio = pd.read_csv('data/analytics/biometric_agg.csv')
    demo = pd.read_csv('data/analytics/demographic_agg.csv')
    
    for df in [enrol, bio, demo]:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
    
    return enrol, bio, demo


def analyze_month_gaps(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 1. MONTH-WISE DATA PRESENCE BY STATE")
    print("#"*70)
    
    all_months = ['2025-03', '2025-04', '2025-05', '2025-06', '2025-07', 
                  '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01']
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        state_month = df.groupby(['state', 'month']).size().unstack(fill_value=0)
        
        print("\nStates with MISSING months:")
        for state in sorted(df['state'].unique()):
            if state in state_month.index:
                present = [str(m) for m in state_month.columns if state_month.loc[state, m] > 0]
                missing = [m for m in all_months if m not in present]
                if missing:
                    print(f"  {state}: missing {missing}")


def analyze_daily_gaps(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 2. DAILY GAPS WITHIN ACTIVE MONTHS")
    print("#"*70)
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        df['_ym'] = df['date'].dt.to_period('M')
        month_days = df.groupby('_ym')['date'].nunique()
        
        print("\nDays with data per month:")
        for m in sorted(month_days.index):
            days_in_month = m.days_in_month
            days_present = month_days[m]
            pct = days_present / days_in_month * 100
            status = "FULL" if pct > 90 else "PARTIAL" if pct > 50 else "SPARSE"
            print(f"  {m}: {days_present}/{days_in_month} days ({pct:.0f}%) [{status}]")


def analyze_state_coverage(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 3. STATE-LEVEL DAILY COVERAGE (Sep-Dec 2025)")
    print("#"*70)
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name} - Sep to Dec 2025")
        print('='*60)
        
        df_active = df[(df['date'] >= '2025-09-01') & (df['date'] <= '2025-12-31')]
        total_days = df_active['date'].nunique()
        
        state_days = df_active.groupby('state')['date'].nunique().sort_values()
        
        print(f"\nTotal unique days in period: {total_days}")
        print(f"\nStates with LOWEST coverage:")
        for state, days in state_days.head(10).items():
            pct = days / total_days * 100
            print(f"  {state}: {days}/{total_days} days ({pct:.0f}%)")


def analyze_district_gaps(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 4. DISTRICT-LEVEL GAPS (Worst offenders)")
    print("#"*70)
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        df_active = df[(df['date'] >= '2025-09-01') & (df['date'] <= '2025-12-31')]
        total_days = df_active['date'].nunique()
        
        dist_days = df_active.groupby(['state', 'district'])['date'].nunique()
        
        poor = dist_days[dist_days < total_days * 0.5].sort_values()
        
        print(f"\nDistricts with <50% day coverage ({len(poor)} total):")
        for (state, dist), days in poor.head(20).items():
            pct = days / total_days * 100
            print(f"  {state[:20]:20} | {dist[:25]:25} | {days}/{total_days} ({pct:.0f}%)")


def analyze_pincode_patterns(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 5. PINCODE ACTIVITY PATTERNS")
    print("#"*70)
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        pin_days = df.groupby('pincode')['date'].nunique()
        
        print(f"\nPincode activity distribution:")
        print(f"  1 day only: {(pin_days == 1).sum():,} pincodes")
        print(f"  2-5 days: {((pin_days > 1) & (pin_days <= 5)).sum():,} pincodes")
        print(f"  6-30 days: {((pin_days > 5) & (pin_days <= 30)).sum():,} pincodes")
        print(f"  31-60 days: {((pin_days > 30) & (pin_days <= 60)).sum():,} pincodes")
        print(f"  60+ days: {(pin_days > 60).sum():,} pincodes")
        
        single_day = pin_days[pin_days == 1].index
        if len(single_day) > 0:
            sample_pins = list(single_day[:5])
            print(f"\n  Sample single-day pincodes:")
            for pin in sample_pins:
                row = df[df['pincode'] == pin].iloc[0]
                print(f"    {pin} | {row['state'][:15]} | {row['district'][:20]} | {row['date'].date()}")


def analyze_volume_anomalies(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 6. VOLUME ANOMALIES BY DATE")
    print("#"*70)
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        daily_vol = df.groupby('date')['total'].sum()
        daily_rows = df.groupby('date').size()
        
        mean_vol = daily_vol.mean()
        mean_rows = daily_rows.mean()
        
        low_vol = daily_vol[daily_vol < mean_vol * 0.1]
        low_rows = daily_rows[daily_rows < mean_rows * 0.1]
        
        print(f"\nDays with <10% of mean volume ({len(low_vol)}):")
        for d, v in low_vol.sort_values().head(10).items():
            print(f"  {d.date()}: {v:,} (mean: {mean_vol:,.0f})")
        
        print(f"\nDays with <10% of mean rows ({len(low_rows)}):")
        for d, r in low_rows.sort_values().head(10).items():
            print(f"  {d.date()}: {r:,} rows (mean: {mean_rows:,.0f})")


def analyze_cross_dataset_gaps(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 7. CROSS-DATASET GAP COMPARISON")
    print("#"*70)
    
    e_dates = set(enrol['date'].unique())
    b_dates = set(bio['date'].unique())
    d_dates = set(demo['date'].unique())
    
    print(f"\nDate coverage:")
    print(f"  Enrolment: {len(e_dates)} dates")
    print(f"  Biometric: {len(b_dates)} dates")
    print(f"  Demographic: {len(d_dates)} dates")
    print(f"  Common to all: {len(e_dates & b_dates & d_dates)} dates")
    
    print(f"\nDates in Biometric but NOT in Enrolment: {len(b_dates - e_dates)}")
    print(f"Dates in Biometric but NOT in Demographic: {len(b_dates - d_dates)}")
    
    print(f"\nState coverage comparison (significant differences):")
    e_states = enrol.groupby('state')['date'].nunique()
    b_states = bio.groupby('state')['date'].nunique()
    d_states = demo.groupby('state')['date'].nunique()
    
    for state in sorted(enrol['state'].unique()):
        e = e_states.get(state, 0)
        b = b_states.get(state, 0)
        d = d_states.get(state, 0)
        if max(e, b, d) - min(e, b, d) > 20:
            print(f"  {state[:25]:25} | E:{e:3} | B:{b:3} | D:{d:3}")


def run_gap_analysis():
    print("="*70)
    print("BRUTAL DATA GAP ANALYSIS")
    print("="*70)
    
    enrol, bio, demo = load_data()
    
    analyze_month_gaps(enrol, bio, demo)
    analyze_daily_gaps(enrol, bio, demo)
    analyze_state_coverage(enrol, bio, demo)
    analyze_district_gaps(enrol, bio, demo)
    analyze_pincode_patterns(enrol, bio, demo)
    analyze_volume_anomalies(enrol, bio, demo)
    analyze_cross_dataset_gaps(enrol, bio, demo)
    
    print("\n" + "="*70)
    print("GAP ANALYSIS COMPLETE")
    print("="*70)


if __name__ == '__main__':
    import os
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    run_gap_analysis()
