"""
UIDAI Hackathon - Killer Metrics Calculator
5 Provocative, Defensible Metrics That Force Conclusions
"""

import pandas as pd
import numpy as np


def load_clean_data():
    enrol = pd.read_csv('data/analytics/enrolment_agg.csv')
    bio = pd.read_csv('data/analytics/biometric_agg.csv')
    demo = pd.read_csv('data/analytics/demographic_agg.csv')
    return enrol, bio, demo


def calculate_killer_metrics():
    enrol, bio, demo = load_clean_data()
    
    # State-level aggregations
    e_state = enrol.groupby('state').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total': 'sum'
    })
    
    b_state = bio.groupby('state')['total'].sum()
    d_state = demo.groupby('state')['total'].sum()
    
    # Create master dataframe
    metrics = pd.DataFrame(index=e_state.index)
    metrics['enrolments'] = e_state['total']
    metrics['biometric_updates'] = b_state
    metrics['demographic_updates'] = d_state
    metrics['adult_enrolments'] = e_state['age_18_greater']
    metrics['child_enrolments'] = e_state['age_0_5'] + e_state['age_5_17']
    
    metrics = metrics.fillna(0)
    
    print("="*70)
    print("KILLER METRICS CALCULATION")
    print("="*70)
    
    # METRIC 1: Update Intensity Index (UII)
    metrics['UII'] = (metrics['biometric_updates'] + metrics['demographic_updates']) / metrics['enrolments']
    print(f"\n1. UPDATE INTENSITY INDEX (UII)")
    print(f"   National Average: {metrics['UII'].mean():.1f}x")
    print(f"   Range: {metrics['UII'].min():.1f}x to {metrics['UII'].max():.1f}x")
    
    # METRIC 2: Identity Maintenance Ratio (IMR)
    metrics['IMR'] = metrics['biometric_updates'] / (metrics['demographic_updates'] + 0.1)
    print(f"\n2. IDENTITY MAINTENANCE RATIO (IMR)")
    print(f"   >2 = Biometric-heavy, <1 = Demographic-heavy")
    
    # METRIC 3: Enrolment Saturation Signal (ESS)
    metrics['ESS'] = (metrics['adult_enrolments'] / metrics['enrolments'] * 100)
    print(f"\n3. ENROLMENT SATURATION SIGNAL (ESS)")
    print(f"   National Average: {metrics['ESS'].mean():.1f}%")
    
    # METRIC 4: Silent Risk Score (SRS)
    metrics['pop_rank'] = metrics['enrolments'].rank(ascending=False)
    metrics['uii_rank'] = metrics['UII'].rank(ascending=True)
    metrics['SRS'] = metrics['pop_rank'] / metrics['uii_rank']
    print(f"\n4. SILENT RISK SCORE (SRS)")
    print(f"   High population + Low updates = High risk")
    
    # METRIC 5: Infrastructure Phase Indicator (IPI)
    child_pct = metrics['child_enrolments'] / metrics['enrolments'] * 100
    uii_norm = (metrics['UII'] - metrics['UII'].min()) / (metrics['UII'].max() - metrics['UII'].min())
    imr_dev = np.abs(metrics['IMR'] - metrics['IMR'].median()) / metrics['IMR'].std()
    
    metrics['IPI'] = (child_pct * 0.4) + (uii_norm * 30) + (imr_dev * 30)
    
    def classify_phase(ipi):
        if ipi < 50:
            return "Phase 1: Still Enrolling"
        elif ipi < 70:
            return "Phase 2: Transitioning"
        else:
            return "Phase 3: Maintenance Mode"
    
    metrics['Phase'] = metrics['IPI'].apply(classify_phase)
    
    print(f"\n5. INFRASTRUCTURE PHASE INDICATOR (IPI)")
    print(f"   Phase 1: Still enrolling, Phase 2: Transitioning, Phase 3: Maintenance mode")
    
    return metrics


def print_provocative_findings(metrics):
    print("\n" + "="*70)
    print("PROVOCATIVE FINDINGS")
    print("="*70)
    
    # UII extremes
    uii_max = metrics['UII'].idxmax()
    uii_min = metrics['UII'].idxmin()
    print(f"\nUPDATE INTENSITY DIVIDE:")
    print(f"   {uii_max}: {metrics.loc[uii_max, 'UII']:.1f}x updates per enrolment")
    print(f"   {uii_min}: {metrics.loc[uii_min, 'UII']:.1f}x updates per enrolment")
    print(f"   RATIO: {metrics.loc[uii_max, 'UII'] / metrics.loc[uii_min, 'UII']:.0f}x difference")
    
    # ESS extremes
    ess_max = metrics['ESS'].idxmax()
    saturated = metrics[metrics['ESS'] < 5]
    print(f"\nSATURATION ANOMALY:")
    print(f"   {ess_max}: {metrics.loc[ess_max, 'ESS']:.1f}% adult enrolments (STILL ENROLLING)")
    print(f"   {len(saturated)} states have <5% adult enrolments (SATURATED)")
    
    # Silent Risk
    high_risk = metrics.nlargest(5, 'SRS')
    print(f"\nSILENT RISK STATES (High population, Low updates):")
    for state, row in high_risk.iterrows():
        print(f"   {state}: Pop rank #{row['pop_rank']:.0f}, UII rank #{row['uii_rank']:.0f} -> Risk: {row['SRS']:.1f}")
    
    # IMR extremes
    bio_heavy = metrics.nlargest(5, 'IMR')
    demo_heavy = metrics.nsmallest(5, 'IMR')
    print(f"\nIDENTITY MAINTENANCE DIVIDE:")
    print(f"   BIOMETRIC-HEAVY (aging populations):")
    for state, row in bio_heavy.iterrows():
        print(f"     {state}: {row['IMR']:.1f}x more biometric than demographic")
    print(f"   DEMOGRAPHIC-HEAVY (migration corridors):")
    for state, row in demo_heavy.iterrows():
        print(f"     {state}: {row['IMR']:.2f}x (more demographic than biometric)")
    
    # Phase distribution
    phase_counts = metrics['Phase'].value_counts()
    print(f"\nINFRASTRUCTURE PHASES:")
    for phase, count in phase_counts.items():
        print(f"   {phase}: {count} states")


def save_metrics(metrics):
    output = metrics.round(2)
    output.to_csv('data/analytics/killer_metrics.csv')
    print(f"\nSaved killer_metrics.csv")
    
    summary = output[['UII', 'IMR', 'ESS', 'SRS', 'Phase']].copy()
    summary = summary.sort_values('UII', ascending=False)
    
    print(f"\nKILLER METRICS SUMMARY:")
    print(summary.to_string())
    
    return summary


def run_killer_metrics():
    print("CALCULATING KILLER METRICS...")
    
    metrics = calculate_killer_metrics()
    print_provocative_findings(metrics)
    summary = save_metrics(metrics)
    
    print("\n" + "="*70)
    print("BRUTAL TRUTH: The data doesn't lie.")
    print("India's Aadhaar system has quietly transitioned phases.")
    print("Policy hasn't caught up.")
    print("="*70)
    
    return metrics, summary


if __name__ == '__main__':
    import os
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    metrics, summary = run_killer_metrics()
