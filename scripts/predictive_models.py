"""
UIDAI Hackathon - Brutal Predictive Models
ETL Pipeline for Forecasting Update Demand
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
    print("ETL PIPELINE: PREPARING PREDICTIVE DATA")
    print("="*70)
    
    # Load clean data
    bio = pd.read_csv('data/analytics/biometric_agg.csv')
    demo = pd.read_csv('data/analytics/demographic_agg.csv')
    enrol = pd.read_csv('data/analytics/enrolment_agg.csv')
    
    # Convert dates
    bio['date'] = pd.to_datetime(bio['date'])
    demo['date'] = pd.to_datetime(demo['date'])
    enrol['date'] = pd.to_datetime(enrol['date'])
    
    print(f"Loaded data:")
    print(f"  Biometric: {len(bio):,} rows")
    print(f"  Demographic: {len(demo):,} rows")
    print(f"  Enrolment: {len(enrol):,} rows")
    
    # Create monthly aggregations for stable forecasting
    bio_monthly = bio.groupby([bio['date'].dt.to_period('M'), 'state']).agg({
        'total': 'sum'
    }).reset_index()
    bio_monthly.columns = ['month', 'state', 'bio_total']
    
    demo_monthly = demo.groupby([demo['date'].dt.to_period('M'), 'state']).agg({
        'total': 'sum'
    }).reset_index()
    demo_monthly.columns = ['month', 'state', 'demo_total']
    
    enrol_monthly = enrol.groupby([enrol['date'].dt.to_period('M'), 'state']).agg({
        'total': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    enrol_monthly.columns = ['month', 'state', 'enrol_total', 'adult_enrol']
    
    # Merge datasets
    monthly_data = bio_monthly.merge(demo_monthly, on=['month', 'state'], how='outer')
    monthly_data = monthly_data.merge(enrol_monthly, on=['month', 'state'], how='outer')
    monthly_data = monthly_data.fillna(0)
    
    # Add time features
    monthly_data['month_str'] = monthly_data['month'].astype(str)
    monthly_data['month_num'] = monthly_data['month'].dt.month
    monthly_data['year'] = monthly_data['month'].dt.year
    
    # Create sequence number for trend analysis
    monthly_data = monthly_data.sort_values(['state', 'month'])
    monthly_data['time_seq'] = monthly_data.groupby('state').cumcount() + 1
    
    print(f"\nMonthly aggregated data: {len(monthly_data):,} rows")
    print(f"Date range: {monthly_data['month'].min()} to {monthly_data['month'].max()}")
    
    return monthly_data


def build_volume_forecasting_model(monthly_data):
    """MODEL 1: 3-Month Volume Forecasting"""
    print(f"\n" + "="*70)
    print("MODEL 1: UPDATE VOLUME FORECASTING")
    print("="*70)
    
    forecasts = []
    model_performance = []
    
    # For each state, build a simple trend model
    for state in monthly_data['state'].unique():
        state_data = monthly_data[monthly_data['state'] == state].copy()
        state_data = state_data.sort_values('month')
        
        if len(state_data) < 6:  # Need minimum data points
            continue
            
        # Prepare features: time sequence, month, recent average
        X = state_data[['time_seq', 'month_num']].values
        y_bio = state_data['bio_total'].values
        y_demo = state_data['demo_total'].values
        
        if len(X) > 3:  # Need enough for train/test
            # Split: use last 2 months for validation
            X_train, X_test = X[:-2], X[-2:]
            y_bio_train, y_bio_test = y_bio[:-2], y_bio[-2:]
            y_demo_train, y_demo_test = y_demo[:-2], y_demo[-2:]
            
            # Fit models
            bio_model = LinearRegression().fit(X_train, y_bio_train)
            demo_model = LinearRegression().fit(X_train, y_demo_train)
            
            # Validate
            bio_pred = bio_model.predict(X_test)
            demo_pred = demo_model.predict(X_test)
            
            bio_mae = mean_absolute_error(y_bio_test, bio_pred)
            demo_mae = mean_absolute_error(y_demo_test, demo_pred)
            
            # Forecast next 3 months
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
            
            model_performance.append({
                'state': state,
                'bio_mae': bio_mae,
                'demo_mae': demo_mae,
                'data_points': len(state_data)
            })
    
    forecast_df = pd.DataFrame(forecasts)
    performance_df = pd.DataFrame(model_performance)
    
    print(f"Built forecasting models for {len(performance_df)} states")
    print(f"Average MAE - Biometric: {performance_df['bio_mae'].mean():,.0f}")
    print(f"Average MAE - Demographic: {performance_df['demo_mae'].mean():,.0f}")
    
    return forecast_df, performance_df


def build_trajectory_classifier(monthly_data):
    """MODEL 2: Update Type Trajectory Prediction"""
    print(f"\n" + "="*70)
    print("MODEL 2: UPDATE TYPE TRAJECTORY")
    print("="*70)
    
    trajectories = []
    
    for state in monthly_data['state'].unique():
        state_data = monthly_data[monthly_data['state'] == state].copy()
        state_data = state_data.sort_values('month')
        
        if len(state_data) < 4:
            continue
            
        # Calculate IMR over time
        state_data['imr'] = (state_data['bio_total'] + 0.1) / (state_data['demo_total'] + 0.1)
        
        # Fit trend line to IMR
        X = state_data['time_seq'].values.reshape(-1, 1)
        y = state_data['imr'].values
        
        if len(X) > 2:
            model = LinearRegression().fit(X, y)
            trend_slope = model.coef_[0]
            current_imr = y[-1]
            
            # Predict IMR in 6 months
            future_seq = state_data['time_seq'].max() + 6
            predicted_imr = model.predict([[future_seq]])[0]
            
            # Classify trajectory
            if trend_slope > 0.05:
                trajectory = "Becoming Biometric-Heavy"
            elif trend_slope < -0.05:
                trajectory = "Becoming Demographic-Heavy"
            else:
                trajectory = "Stable Pattern"
            
            # Classify current state
            if current_imr > 2:
                current_type = "Biometric-Heavy"
            elif current_imr < 1:
                current_type = "Demographic-Heavy"
            else:
                current_type = "Balanced"
            
            trajectories.append({
                'state': state,
                'current_imr': current_imr,
                'predicted_imr': predicted_imr,
                'trend_slope': trend_slope,
                'current_type': current_type,
                'trajectory': trajectory,
                'confidence': min(1.0, abs(trend_slope) * 10)  # Simple confidence
            })
    
    trajectory_df = pd.DataFrame(trajectories)
    
    print(f"Classified trajectories for {len(trajectory_df)} states")
    
    # Summary
    trajectory_counts = trajectory_df['trajectory'].value_counts()
    print(f"\nTrajectory distribution:")
    for traj, count in trajectory_counts.items():
        print(f"  {traj}: {count} states")
    
    return trajectory_df


def build_saturation_predictor(monthly_data):
    """MODEL 3: Adult Saturation Timeline"""
    print(f"\n" + "="*70)
    print("MODEL 3: SATURATION TIMELINE PREDICTION")
    print("="*70)
    
    saturation_predictions = []
    
    for state in monthly_data['state'].unique():
        state_data = monthly_data[monthly_data['state'] == state].copy()
        state_data = state_data[state_data['enrol_total'] > 0]  # Only months with enrolments
        
        if len(state_data) < 3:
            continue
            
        # Calculate adult percentage over time
        state_data['adult_pct'] = (state_data['adult_enrol'] / state_data['enrol_total'] * 100)
        
        # Remove outliers (>50% adult - likely data issues)
        state_data = state_data[state_data['adult_pct'] <= 50]
        
        if len(state_data) < 3:
            continue
            
        current_adult_pct = state_data['adult_pct'].iloc[-1]
        
        # If already saturated (<5%), mark as saturated
        if current_adult_pct < 5:
            status = "Already Saturated"
            months_to_saturation = 0
        else:
            # Fit exponential decay model
            X = state_data['time_seq'].values.reshape(-1, 1)
            y = state_data['adult_pct'].values
            
            if len(X) > 2 and y.std() > 1:  # Need variation to fit
                model = LinearRegression().fit(X, y)
                trend_slope = model.coef_[0]
                
                if trend_slope < -0.1:  # Declining
                    # Predict when it hits 5%
                    current_seq = state_data['time_seq'].max()
                    months_to_saturation = max(0, (current_adult_pct - 5) / abs(trend_slope))
                    status = "Approaching Saturation"
                else:
                    months_to_saturation = 999  # Very long time
                    status = "Still Enrolling"
            else:
                months_to_saturation = 999
                status = "Stable/Unclear"
        
        saturation_predictions.append({
            'state': state,
            'current_adult_pct': current_adult_pct,
            'status': status,
            'months_to_saturation': months_to_saturation,
            'estimated_saturation_date': '2026-12' if months_to_saturation < 12 else '2027+'
        })
    
    saturation_df = pd.DataFrame(saturation_predictions)
    
    print(f"Analyzed saturation for {len(saturation_df)} states")
    
    status_counts = saturation_df['status'].value_counts()
    print(f"\nSaturation status:")
    for status, count in status_counts.items():
        print(f"  {status}: {count} states")
    
    return saturation_df


def generate_brutal_insights(forecast_df, trajectory_df, saturation_df):
    """Generate brutal predictive insights"""
    print(f"\n" + "="*70)
    print("BRUTAL PREDICTIVE INSIGHTS")
    print("="*70)
    
    # High-demand states for next quarter
    q1_2026 = forecast_df[forecast_df['forecast_month'].isin(['2026-01', '2026-02', '2026-03'])]
    high_demand = q1_2026.groupby('state')['total_forecast'].sum().sort_values(ascending=False)
    
    print(f"\nQ1 2026 UPDATE DEMAND FORECAST:")
    print(f"States needing most update capacity:")
    for state, demand in high_demand.head(10).items():
        print(f"  {state[:30]:30} | {demand:>10,.0f} updates")
    
    # Trajectory shifts
    shifting_states = trajectory_df[trajectory_df['trajectory'] != 'Stable Pattern']
    print(f"\nSTATES CHANGING UPDATE PATTERNS:")
    for _, row in shifting_states.head(10).iterrows():
        print(f"  {row['state'][:30]:30} | {row['trajectory']} (IMR: {row['current_imr']:.2f} → {row['predicted_imr']:.2f})")
    
    # Saturation timeline
    approaching = saturation_df[saturation_df['status'] == 'Approaching Saturation']
    still_enrolling = saturation_df[saturation_df['status'] == 'Still Enrolling']
    
    print(f"\nSATURATION TIMELINE:")
    print(f"  Already saturated: {len(saturation_df[saturation_df['status'] == 'Already Saturated'])} states")
    print(f"  Approaching saturation: {len(approaching)} states")
    print(f"  Still enrolling: {len(still_enrolling)} states")
    
    if len(still_enrolling) > 0:
        print(f"\nStates still in enrolment phase:")
        for _, row in still_enrolling.iterrows():
            print(f"  {row['state'][:30]:30} | {row['current_adult_pct']:.1f}% adult enrolments")


def save_predictions(forecast_df, trajectory_df, saturation_df):
    """Save all predictions"""
    forecast_df.to_csv('data/analytics/volume_forecasts.csv', index=False)
    trajectory_df.to_csv('data/analytics/trajectory_predictions.csv', index=False)
    saturation_df.to_csv('data/analytics/saturation_predictions.csv', index=False)
    
    print(f"\nSaved predictions:")
    print(f"  volume_forecasts.csv")
    print(f"  trajectory_predictions.csv") 
    print(f"  saturation_predictions.csv")


def run_predictive_pipeline():
    """Execute full predictive modeling pipeline"""
    print("BRUTAL PREDICTIVE MODELING PIPELINE")
    
    # ETL
    monthly_data = load_and_prepare_data()
    
    # Build models
    forecast_df, performance_df = build_volume_forecasting_model(monthly_data)
    trajectory_df = build_trajectory_classifier(monthly_data)
    saturation_df = build_saturation_predictor(monthly_data)
    
    # Generate insights
    generate_brutal_insights(forecast_df, trajectory_df, saturation_df)
    
    # Save results
    save_predictions(forecast_df, trajectory_df, saturation_df)
    
    print(f"\n" + "="*70)
    print("PREDICTIVE PIPELINE COMPLETE")
    print("="*70)
    
    return forecast_df, trajectory_df, saturation_df, monthly_data


if __name__ == '__main__':
    import os
    os.chdir('/home/btwitsvoid/Documents/ML Project/uidaihack')
    forecast_df, trajectory_df, saturation_df, monthly_data = run_predictive_pipeline()
