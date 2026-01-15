"""
UIDAI Hackathon - Brutal Gap Analysis for Main Dataset
"""

import pandas as pd
import numpy as np


def load_main_data():
    enrol = pd.read_csv('data/enrolment.csv')
    bio = pd.read_csv('data/biometric.csv')
    demo = pd.read_csv('data/demographic.csv')
    
    for df in [enrol, bio, demo]:
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
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
        missing_count = 0
        for state in sorted(df['state'].unique()):
            if state in state_month.index:
                present = [str(m) for m in state_month.columns if state_month.loc[state, m] > 0]
                missing = [m for m in all_months if m not in present]
                if missing:
                    missing_count += 1
                    print(f"  {state}: missing {missing}")
        
        if missing_count == 0:
            print("  None - all states have all months")


def analyze_daily_gaps(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 2. DAILY GAPS WITHIN MONTHS")
    print("#"*70)
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        month_days = df.groupby(df['date'].dt.to_period('M'))['date'].nunique()
        
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
        print(f"{name}")
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
    print("# 4. DISTRICT-LEVEL GAPS")
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
        for (state, dist), days in poor.head(25).items():
            pct = days / total_days * 100
            print(f"  {state[:20]:20} | {dist[:25]:25} | {days}/{total_days} ({pct:.0f}%)")


def analyze_volume_anomalies(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 5. VOLUME ANOMALIES BY DATE")
    print("#"*70)
    
    for name, df, total_col in [
        ('ENROLMENT', enrol, ['age_0_5', 'age_5_17', 'age_18_greater']),
        ('BIOMETRIC', bio, ['bio_age_5_17', 'bio_age_17_']),
        ('DEMOGRAPHIC', demo, ['demo_age_5_17', 'demo_age_17_'])
    ]:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        
        df['_total'] = df[total_col].sum(axis=1)
        daily_vol = df.groupby('date')['_total'].sum()
        daily_rows = df.groupby('date').size()
        
        mean_vol = daily_vol.mean()
        mean_rows = daily_rows.mean()
        
        low_vol = daily_vol[daily_vol < mean_vol * 0.1]
        high_vol = daily_vol[daily_vol > mean_vol * 5]
        
        print(f"\nMean daily volume: {mean_vol:,.0f}")
        print(f"Mean daily rows: {mean_rows:,.0f}")
        
        print(f"\nDays with <10% of mean volume ({len(low_vol)}):")
        for d, v in low_vol.sort_values().head(10).items():
            print(f"  {d.date()}: {v:,}")
        
        print(f"\nDays with >5x mean volume ({len(high_vol)}):")
        for d, v in high_vol.sort_values(ascending=False).head(10).items():
            print(f"  {d.date()}: {v:,}")


def analyze_cross_dataset(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 6. CROSS-DATASET COMPARISON")
    print("#"*70)
    
    e_dates = set(enrol['date'].unique())
    b_dates = set(bio['date'].unique())
    d_dates = set(demo['date'].unique())
    
    print(f"\nDate coverage:")
    print(f"  Enrolment: {len(e_dates)} dates")
    print(f"  Biometric: {len(b_dates)} dates")
    print(f"  Demographic: {len(d_dates)} dates")
    print(f"  Common to all: {len(e_dates & b_dates & d_dates)} dates")
    
    print(f"\nDates ONLY in Biometric (not in others): {len(b_dates - e_dates - d_dates)}")
    
    # State coverage comparison
    print(f"\nState coverage (dates per state):")
    e_states = enrol.groupby('state')['date'].nunique()
    b_states = bio.groupby('state')['date'].nunique()
    d_states = demo.groupby('state')['date'].nunique()
    
    print(f"\n{'State':<30} | {'Enrol':>5} | {'Bio':>5} | {'Demo':>5} | {'Gap':>5}")
    print("-"*60)
    for state in sorted(enrol['state'].unique()):
        e = e_states.get(state, 0)
        b = b_states.get(state, 0)
        d = d_states.get(state, 0)
        gap = max(e, b, d) - min(e, b, d)
        if gap > 10:
            print(f"  {state[:28]:<28} | {e:>5} | {b:>5} | {d:>5} | {gap:>5}")


def analyze_duplicates_remaining(enrol, bio, demo):
    print("\n" + "#"*70)
    print("# 7. DUPLICATE CHECK (Main Dataset)")
    print("#"*70)
    
    KEY_COLS = ['date', 'state', 'district', 'pincode']
    
    for name, df in [('ENROLMENT', enrol), ('BIOMETRIC', bio), ('DEMOGRAPHIC', demo)]:
        print(f"\n{name}:")
        exact = df.duplicated().sum()
        key_dupes = df.duplicated(subset=KEY_COLS).sum()
        print(f"  Exact duplicates: {exact:,}")
        print(f"  Key duplicates: {key_dupes:,}")


def run_main_gap_analysis():
    print("="*70)
    print("BRUTAL GAP ANALYSIS - MAIN DATASET")
    print("="*70)
    
    enrol, bio, demo = load_main_data()
    
    print(f"\nDataset sizes:")
    print(f"  Enrolment: {len(enrol):,} rows")
    print(f"  Biometric: {len(bio):,} rows")
    print(f"  Demographic: {len(demo):,} rows")
    
    analyze_month_gaps(enrol, bio, demo)
    analyze_daily_gaps(enrol, bio, demo)
    analyze_state_coverage(enrol, bio, demo)
    analyze_district_gaps(enrol, bio, demo)
    analyze_volume_anomalies(enrol, bio, demo)
    analyze_cross_dataset(enrol, bio, demo)
    analyze_duplicates_remaining(enrol, bio, demo)
    
    print("\n" + "="*70)
    print("GAP ANALYSIS COMPLETE")
    print("="*70)


if __name__ == '__main__':
    import os
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    run_main_gap_analysis()
