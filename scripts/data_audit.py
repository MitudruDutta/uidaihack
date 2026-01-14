"""
UIDAI Hackathon - Brutal Data Audit
Dense analysis of all 3 datasets before cleaning
"""

import pandas as pd
import numpy as np
from collections import Counter

def load_datasets():
    """Load all 3 datasets"""
    enrol = pd.read_csv('data/enrolment.csv')
    bio = pd.read_csv('data/biometric.csv')
    demo = pd.read_csv('data/demographic.csv')
    return enrol, bio, demo

def basic_stats(df, name):
    """Basic dataset statistics"""
    print(f"\n{'='*70}")
    print(f"DATASET: {name.upper()}")
    print('='*70)
    print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData Types:\n{df.dtypes.to_string()}")

def missing_analysis(df, name):
    """Analyze missing values"""
    print(f"\n--- MISSING VALUES ({name}) ---")
    missing = df.isnull().sum()
    total_missing = missing.sum()
    if total_missing == 0:
        print("No missing values")
    else:
        for col in missing[missing > 0].index:
            pct = missing[col] / len(df) * 100
            print(f"  {col}: {missing[col]:,} ({pct:.2f}%)")

def duplicate_analysis(df, name):
    """Analyze duplicates in detail"""
    print(f"\n--- DUPLICATE ANALYSIS ({name}) ---")
    
    # Exact duplicates
    exact_dupes = df.duplicated().sum()
    print(f"Exact duplicates: {exact_dupes:,} ({exact_dupes/len(df)*100:.2f}%)")
    
    # Duplicates by key columns
    key_cols = ['date', 'state', 'district', 'pincode']
    key_dupes = df.duplicated(subset=key_cols).sum()
    print(f"Duplicates by {key_cols}: {key_dupes:,} ({key_dupes/len(df)*100:.2f}%)")
    
    # Show sample duplicates
    if exact_dupes > 0:
        print(f"\nSample duplicate rows:")
        dupe_mask = df.duplicated(keep=False)
        sample = df[dupe_mask].head(10)
        print(sample.to_string())

def date_analysis(df, name):
    """Analyze date column"""
    print(f"\n--- DATE ANALYSIS ({name}) ---")
    df['_date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    invalid = df['_date'].isnull().sum()
    print(f"Invalid dates: {invalid}")
    print(f"Date range: {df['_date'].min()} to {df['_date'].max()}")
    print(f"Unique dates: {df['_date'].nunique()}")
    
    # Monthly distribution
    df['_month'] = df['_date'].dt.to_period('M')
    monthly = df['_month'].value_counts().sort_index()
    print(f"\nMonthly distribution:")
    for m, c in monthly.items():
        print(f"  {m}: {c:,}")
    
    df.drop(['_date', '_month'], axis=1, inplace=True)

def state_analysis(df, name):
    """Analyze state column"""
    print(f"\n--- STATE ANALYSIS ({name}) ---")
    print(f"Unique states: {df['state'].nunique()}")
    
    state_counts = df['state'].value_counts()
    print(f"\nTop 10 states by records:")
    for s, c in state_counts.head(10).items():
        print(f"  {s}: {c:,}")
    
    print(f"\nBottom 5 states by records:")
    for s, c in state_counts.tail(5).items():
        print(f"  {s}: {c:,}")

def district_analysis(df, name):
    """Analyze district column"""
    print(f"\n--- DISTRICT ANALYSIS ({name}) ---")
    print(f"Unique districts: {df['district'].nunique()}")
    
    # Districts per state
    dist_per_state = df.groupby('state')['district'].nunique().sort_values(ascending=False)
    print(f"\nDistricts per state (top 10):")
    for s, c in dist_per_state.head(10).items():
        print(f"  {s}: {c}")
    
    # Check for district name inconsistencies
    districts = df['district'].unique()
    potential_issues = []
    for d in districts:
        if d != d.strip():
            potential_issues.append(f"Whitespace: '{d}'")
        if d.isupper() or d.islower():
            potential_issues.append(f"Case issue: '{d}'")
    
    if potential_issues:
        print(f"\nPotential district name issues:")
        for issue in potential_issues[:10]:
            print(f"  {issue}")

def pincode_analysis(df, name):
    """Analyze pincode column"""
    print(f"\n--- PINCODE ANALYSIS ({name}) ---")
    print(f"Unique pincodes: {df['pincode'].nunique()}")
    
    # Validate pincode format (6 digits, 100000-999999)
    invalid_pins = ((df['pincode'] < 100000) | (df['pincode'] > 999999)).sum()
    print(f"Invalid pincodes (not 6 digits): {invalid_pins}")
    
    # Pincodes per state
    pins_per_state = df.groupby('state')['pincode'].nunique().sort_values(ascending=False)
    print(f"\nPincodes per state (top 10):")
    for s, c in pins_per_state.head(10).items():
        print(f"  {s}: {c}")

def numeric_analysis(df, name, num_cols):
    """Deep analysis of numeric columns"""
    print(f"\n--- NUMERIC ANALYSIS ({name}) ---")
    
    for col in num_cols:
        print(f"\n{col}:")
        print(f"  Min: {df[col].min()}")
        print(f"  Max: {df[col].max():,}")
        print(f"  Mean: {df[col].mean():.2f}")
        print(f"  Median: {df[col].median():.2f}")
        print(f"  Std: {df[col].std():.2f}")
        print(f"  Zeros: {(df[col] == 0).sum():,} ({(df[col] == 0).sum()/len(df)*100:.1f}%)")
        print(f"  Negatives: {(df[col] < 0).sum()}")
        
        # Percentiles
        percentiles = df[col].quantile([0.25, 0.5, 0.75, 0.90, 0.95, 0.99])
        print(f"  Percentiles: 25%={percentiles[0.25]:.0f}, 50%={percentiles[0.5]:.0f}, 75%={percentiles[0.75]:.0f}, 90%={percentiles[0.90]:.0f}, 95%={percentiles[0.95]:.0f}, 99%={percentiles[0.99]:.0f}")
        
        # Outliers (IQR method)
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
        print(f"  Outliers (IQR): {outliers:,} ({outliers/len(df)*100:.2f}%)")

def cross_dataset_analysis(enrol, bio, demo):
    """Compare across datasets"""
    print(f"\n{'='*70}")
    print("CROSS-DATASET ANALYSIS")
    print('='*70)
    
    # State overlap
    enrol_states = set(enrol['state'].unique())
    bio_states = set(bio['state'].unique())
    demo_states = set(demo['state'].unique())
    
    print(f"\nStates in all datasets: {len(enrol_states & bio_states & demo_states)}")
    print(f"States only in enrolment: {enrol_states - bio_states - demo_states}")
    print(f"States only in biometric: {bio_states - enrol_states - demo_states}")
    print(f"States only in demographic: {demo_states - enrol_states - bio_states}")
    
    # District overlap
    enrol_dist = set(enrol['district'].unique())
    bio_dist = set(bio['district'].unique())
    demo_dist = set(demo['district'].unique())
    
    print(f"\nDistricts in all datasets: {len(enrol_dist & bio_dist & demo_dist)}")
    print(f"Districts only in enrolment: {len(enrol_dist - bio_dist - demo_dist)}")
    print(f"Districts only in biometric: {len(bio_dist - enrol_dist - demo_dist)}")
    print(f"Districts only in demographic: {len(demo_dist - enrol_dist - bio_dist)}")
    
    # Pincode overlap
    enrol_pins = set(enrol['pincode'].unique())
    bio_pins = set(bio['pincode'].unique())
    demo_pins = set(demo['pincode'].unique())
    
    print(f"\nPincodes in all datasets: {len(enrol_pins & bio_pins & demo_pins)}")
    print(f"Pincodes only in enrolment: {len(enrol_pins - bio_pins - demo_pins)}")
    print(f"Pincodes only in biometric: {len(bio_pins - enrol_pins - demo_pins)}")
    print(f"Pincodes only in demographic: {len(demo_pins - enrol_pins - bio_pins)}")
    
    # Date overlap
    enrol['_date'] = pd.to_datetime(enrol['date'], format='%d-%m-%Y')
    bio['_date'] = pd.to_datetime(bio['date'], format='%d-%m-%Y')
    demo['_date'] = pd.to_datetime(demo['date'], format='%d-%m-%Y')
    
    enrol_dates = set(enrol['_date'].unique())
    bio_dates = set(bio['_date'].unique())
    demo_dates = set(demo['_date'].unique())
    
    print(f"\nDates in all datasets: {len(enrol_dates & bio_dates & demo_dates)}")
    print(f"Dates only in enrolment: {len(enrol_dates - bio_dates - demo_dates)}")
    print(f"Dates only in biometric: {len(bio_dates - enrol_dates - demo_dates)}")
    print(f"Dates only in demographic: {len(demo_dates - enrol_dates - bio_dates)}")
    
    enrol.drop('_date', axis=1, inplace=True)
    bio.drop('_date', axis=1, inplace=True)
    demo.drop('_date', axis=1, inplace=True)

def aggregation_analysis(df, name, num_cols):
    """Analyze aggregated totals"""
    print(f"\n--- AGGREGATION ANALYSIS ({name}) ---")
    
    df['_total'] = df[num_cols].sum(axis=1)
    
    # State-level totals
    state_totals = df.groupby('state')['_total'].sum().sort_values(ascending=False)
    print(f"\nState-level totals (top 10):")
    for s, t in state_totals.head(10).items():
        print(f"  {s}: {t:,}")
    
    print(f"\nState-level totals (bottom 5):")
    for s, t in state_totals.tail(5).items():
        print(f"  {s}: {t:,}")
    
    # Grand total
    print(f"\nGrand total: {df['_total'].sum():,}")
    
    df.drop('_total', axis=1, inplace=True)

def value_distribution(df, name, num_cols):
    """Analyze value distributions"""
    print(f"\n--- VALUE DISTRIBUTION ({name}) ---")
    
    for col in num_cols:
        print(f"\n{col} value counts (top 10):")
        vc = df[col].value_counts().head(10)
        for v, c in vc.items():
            print(f"  {v}: {c:,}")

def run_full_audit():
    """Run complete audit on all datasets"""
    print("="*70)
    print("UIDAI HACKATHON - BRUTAL DATA AUDIT")
    print("="*70)
    
    enrol, bio, demo = load_datasets()
    
    # Enrolment analysis
    basic_stats(enrol, 'enrolment')
    missing_analysis(enrol, 'enrolment')
    duplicate_analysis(enrol, 'enrolment')
    date_analysis(enrol, 'enrolment')
    state_analysis(enrol, 'enrolment')
    district_analysis(enrol, 'enrolment')
    pincode_analysis(enrol, 'enrolment')
    enrol_num_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
    numeric_analysis(enrol, 'enrolment', enrol_num_cols)
    aggregation_analysis(enrol, 'enrolment', enrol_num_cols)
    value_distribution(enrol, 'enrolment', enrol_num_cols)
    
    # Biometric analysis
    basic_stats(bio, 'biometric')
    missing_analysis(bio, 'biometric')
    duplicate_analysis(bio, 'biometric')
    date_analysis(bio, 'biometric')
    state_analysis(bio, 'biometric')
    district_analysis(bio, 'biometric')
    pincode_analysis(bio, 'biometric')
    bio_num_cols = ['bio_age_5_17', 'bio_age_17_']
    numeric_analysis(bio, 'biometric', bio_num_cols)
    aggregation_analysis(bio, 'biometric', bio_num_cols)
    value_distribution(bio, 'biometric', bio_num_cols)
    
    # Demographic analysis
    basic_stats(demo, 'demographic')
    missing_analysis(demo, 'demographic')
    duplicate_analysis(demo, 'demographic')
    date_analysis(demo, 'demographic')
    state_analysis(demo, 'demographic')
    district_analysis(demo, 'demographic')
    pincode_analysis(demo, 'demographic')
    demo_num_cols = ['demo_age_5_17', 'demo_age_17_']
    numeric_analysis(demo, 'demographic', demo_num_cols)
    aggregation_analysis(demo, 'demographic', demo_num_cols)
    value_distribution(demo, 'demographic', demo_num_cols)
    
    # Cross-dataset analysis
    cross_dataset_analysis(enrol, bio, demo)
    
    print("\n" + "="*70)
    print("AUDIT COMPLETE")
    print("="*70)

if __name__ == '__main__':
    import os
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    run_full_audit()
