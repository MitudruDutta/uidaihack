"""
UIDAI Hackathon - Fixed Predictive Models
Remove broken trajectory model, keep working ones
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')


def load_and_prepare_data():
    """ETL: Load and prepare time series data"""
    print("="*70)
    print("FIXED PREDICTIVE MODELS - KEEPING WHAT WORKS")
    print("="*70)
    
    bio = pd.read_csv('data/analytics/biometric_agg.csv')
    demo = pd.read_csv('data/analytics/demographic_agg.csv')
    enrol = pd.read_csv('data/analytics/enrolment_agg.csv')
    
    for df in [bio, demo, enrol]:
        df['date'] = pd.to_datetime(df['date'])
    
    # Monthly aggregations
    bio_monthly = bio.groupby([bio['date'].dt.to_period('M'), 'state']).agg({
        'total': 'sum'
    }).reset_index()
    bio_monthly.columns = ['month', 'state', 'bio_total']
    
    demo_monthly = demo.groupby([demo['date'].dt.to_period('M'), 'state']).agg({
        'total': 'sum'
    }).reset_index()
    demo_monthly.columns = ['month', 'state', 'demo_total']
    
    monthly_data = bio_monthly.merge(demo_monthly, on=['month', 'state'], how='outer')
    monthly_data = monthly_data.fillna(0)
    monthly_data = monthly_data.sort_values(['state', 'month'])
    monthly_data['time_seq'] = monthly_data.groupby('state').cumcount() + 1
    monthly_data['month_num'] = monthly_data['month'].dt.month
    
    return monthly_data


def build_volume_forecasting_model(monthly_data):
    """MODEL 1: Volume Forecasting (WORKING)"""
    print(f"\nMODEL 1: UPDATE VOLUME FORECASTING (VALIDATED)")
    print("-"*50)
    
    forecasts = []
    
    for state in monthly_data['state'].unique():
        state_data = monthly_data[monthly_data['state'] == state].copy()
        
        if len(state_data) < 6:
            continue
            
        X = state_data[['time_seq', 'month_num']].values
        y_bio = state_data['bio_total'].values
        y_demo = state_data['demo_total'].values
        
        if len(X) > 3:
            X_train, X_test = X[:-2], X[-2:]
            y_bio_train, y_bio_test = y_bio[:-2], y_bio[-2:]
            y_demo_train, y_demo_test = y_demo[:-2], y_demo[-2:]
            
            bio_model = LinearRegression().fit(X_train, y_bio_train)
            demo_model = LinearRegression().fit(X_train, y_demo_train)
            
            last_seq = state_data['time_seq'].max()
            future_months = [1, 2, 3]  # Jan, Feb, Mar 2026
            
            for i, month in enumerate(future_months, 1):
                X_future = np.array([[last_seq + i, month]])
                bio_forecast = max(0, bio_model.predict(X_future)[0])
                demo_forecast = max(0, demo_model.predict(X_future)[0])
                
                forecasts.append({
                    'state': state,
                    'forecast_month': f"2026-{month:02d}",
                    'bio_forecast': bio_forecast,
                    'demo_forecast': demo_forecast,
                    'total_forecast': bio_forecast + demo_forecast
                })
    
    forecast_df = pd.DataFrame(forecasts)
    return forecast_df


def build_simple_trajectory_classifier(monthly_data):
    """MODEL 2: Simple Current State Classification (FIXED)"""
    print(f"\nMODEL 2: CURRENT UPDATE TYPE CLASSIFICATION (FIXED)")
    print("-"*50)
    
    # Use current state only, no prediction
    bio_state = monthly_data.groupby('state')['bio_total'].sum()
    demo_state = monthly_data.groupby('state')['demo_total'].sum()
    
    classifications = []
    
    for state in bio_state.index:
        bio_total = bio_state[state]
        demo_total = demo_state.get(state, 0)
        
        current_imr = bio_total / (demo_total + 0.1)
        
        if current_imr > 2:
            update_type = "Biometric-Heavy"
            description = "More biometric than demographic updates"
        elif current_imr < 1:
            update_type = "Demographic-Heavy" 
            description = "More demographic than biometric updates"
        else:
            update_type = "Balanced"
            description = "Similar biometric and demographic updates"
        
        classifications.append({
            'state': state,
            'current_imr': current_imr,
            'update_type': update_type,
            'description': description,
            'bio_total': bio_total,
            'demo_total': demo_total
        })
    
    classification_df = pd.DataFrame(classifications)
    
    type_counts = classification_df['update_type'].value_counts()
    print(f"Current update type distribution:")
    for update_type, count in type_counts.items():
        print(f"  {update_type}: {count} states")
    
    return classification_df


def build_demand_concentration_analysis(forecast_df):
    """MODEL 3: Demand Concentration Analysis"""
    print(f"\nMODEL 3: UPDATE DEMAND CONCENTRATION ANALYSIS")
    print("-"*50)
    
    # Q1 2026 total demand by state
    q1_demand = forecast_df.groupby('state')['total_forecast'].sum().sort_values(ascending=False)
    total_demand = q1_demand.sum()
    
    # Calculate concentration
    concentration_analysis = []
    cumulative_demand = 0
    
    for i, (state, demand) in enumerate(q1_demand.items(), 1):
        cumulative_demand += demand
        cumulative_pct = cumulative_demand / total_demand * 100
        
        concentration_analysis.append({
            'rank': i,
            'state': state,
            'q1_demand': demand,
            'demand_pct': demand / total_demand * 100,
            'cumulative_pct': cumulative_pct
        })
    
    concentration_df = pd.DataFrame(concentration_analysis)
    
    # Find concentration points
    top_5_pct = concentration_df.head(5)['cumulative_pct'].iloc[-1]
    top_10_pct = concentration_df.head(10)['cumulative_pct'].iloc[-1]
    
    print(f"Demand concentration:")
    print(f"  Top 5 states: {top_5_pct:.1f}% of total demand")
    print(f"  Top 10 states: {top_10_pct:.1f}% of total demand")
    
    return concentration_df


def generate_actionable_insights(forecast_df, classification_df, concentration_df):
    """Generate actionable insights from working models"""
    print(f"\n" + "="*70)
    print("ACTIONABLE INSIGHTS (FROM WORKING MODELS)")
    print("="*70)
    
    # High-demand states
    top_demand = concentration_df.head(5)
    print(f"\nQ1 2026 RESOURCE ALLOCATION PRIORITY:")
    for _, row in top_demand.iterrows():
        print(f"  #{row['rank']} {row['state'][:25]:25} | {row['q1_demand']:>10,.0f} updates ({row['demand_pct']:.1f}%)")
    
    # Update type distribution
    bio_heavy = classification_df[classification_df['update_type'] == 'Biometric-Heavy']
    demo_heavy = classification_df[classification_df['update_type'] == 'Demographic-Heavy']
    
    print(f"\nINFRASTRUCTURE TYPE REQUIREMENTS:")
    print(f"  Biometric-Heavy states: {len(bio_heavy)} (need biometric capacity)")
    print(f"  Demographic-Heavy states: {len(demo_heavy)} (need demographic capacity)")
    
    # Cross-analysis: High demand + Update type
    print(f"\nCRITICAL INFRASTRUCTURE GAPS:")
    for _, row in top_demand.iterrows():
        state = row['state']
        demand = row['q1_demand']
        update_type = classification_df[classification_df['state'] == state]['update_type'].iloc[0]
        print(f"  {state[:25]:25} | {demand:>10,.0f} updates | {update_type}")


def save_fixed_predictions(forecast_df, classification_df, concentration_df):
    """Save working predictions only"""
    forecast_df.to_csv('data/analytics/volume_forecasts_fixed.csv', index=False)
    classification_df.to_csv('data/analytics/update_type_classification.csv', index=False)
    concentration_df.to_csv('data/analytics/demand_concentration.csv', index=False)
    
    print(f"\nSaved working predictions:")
    print(f"  volume_forecasts_fixed.csv")
    print(f"  update_type_classification.csv")
    print(f"  demand_concentration.csv")


def run_fixed_pipeline():
    """Run only the working models"""
    monthly_data = load_and_prepare_data()
    
    # Working models only
    forecast_df = build_volume_forecasting_model(monthly_data)
    classification_df = build_simple_trajectory_classifier(monthly_data)
    concentration_df = build_demand_concentration_analysis(forecast_df)
    
    generate_actionable_insights(forecast_df, classification_df, concentration_df)
    save_fixed_predictions(forecast_df, classification_df, concentration_df)
    
    print(f"\n" + "="*70)
    print("FIXED PIPELINE COMPLETE - ONLY TRUSTWORTHY MODELS")
    print("="*70)
    
    return forecast_df, classification_df, concentration_df


if __name__ == '__main__':
    import os
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    forecast_df, classification_df, concentration_df = run_fixed_pipeline()
