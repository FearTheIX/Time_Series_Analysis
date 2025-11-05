"""
Main application for time series analysis and forecasting
Orchestrates the complete analysis workflow
"""

import pandas as pd
import matplotlib.pyplot as plt
from data_loader import DataLoader
from exploratory_analysis import ExploratoryAnalysis
from stationarity_analysis import StationarityAnalysis
from arima_model import ARIMAModel
from config import VALUE_COLUMN

def main():
    print("=== TIME SERIES ANALYSIS OF EXCHANGE RATE DATA ===\n")
    
    # Step 1: Load and prepare data
    print("Step 1: Loading data...")
    loader = DataLoader()
    data = loader.load_data()
    
    if data is None:
        print("Failed to load data. Exiting.")
        return
    
    summary = loader.get_data_summary()
    print("Data loaded successfully!\n")
    
    # Step 2: Exploratory Data Analysis
    print("Step 2: Exploratory Data Analysis...")
    explorer = ExploratoryAnalysis(data)
    
    # Generate plots
    explorer.plot_time_series('results/time_series.png')
    explorer.plot_distribution('results/distribution.png')
    
    # Generate statistics
    stats = explorer.generate_summary_statistics()
    print("\nExploratory Analysis Complete!\n")
    
    # Step 3: Stationarity Analysis
    print("Step 3: Stationarity Analysis...")
    stationarity_analyzer = StationarityAnalysis(data)
    
    # Perform stationarity tests
    stationarity_results = stationarity_analyzer.analyze_stationarity()
    
    # Plot ACF/PACF
    stationarity_analyzer.plot_acf_pacf(data[VALUE_COLUMN], save_path='results/acf_pacf.png')
    
    # Seasonal decomposition
    decomposition = stationarity_analyzer.seasonal_decomposition(save_path='results/decomposition.png')
    print("Stationarity Analysis Complete!\n")
    
    # Step 4: ARIMA Modeling
    print("Step 4: ARIMA Modeling...")
    arima_model = ARIMAModel(data)
    
    # Prepare data (split into train/test)
    arima_model.prepare_data(test_size=0.2)
    
    # Train model with automatic parameter selection
    arima_model.train_model()
    
    # Validate model
    metrics, forecast = arima_model.validate_model()
    
    # Generate plots
    arima_model.plot_validation('results/arima_validation.png')
    arima_model.plot_residuals('results/arima_residuals.png')
    print("ARIMA Modeling Complete!\n")
    
    # Step 5: Generate Final Report
    print("Step 5: Generating Final Report...")
    generate_final_report(summary, stats, stationarity_results, metrics)
    
    print("\n=== ANALYSIS COMPLETE ===")
    print("Check the 'results' folder for all generated plots and analysis.")

def generate_final_report(summary, stats, stationarity_results, metrics):
    """Generate a comprehensive final report"""
    
    report = f"""
    FINAL ANALYSIS REPORT
    ====================
    
    DATA SUMMARY:
    -------------
    Total Records: {summary['total_records']}
    Date Range: {summary['date_range'][0]} to {summary['date_range'][1]}
    Missing Values: {summary['missing_values']}
    
    BASIC STATISTICS:
    ----------------
    Mean: {stats['Basic Statistics']['mean']:.4f}
    Standard Deviation: {stats['Basic Statistics']['std']:.4f}
    Minimum: {stats['Basic Statistics']['min']:.4f}
    Maximum: {stats['Basic Statistics']['max']:.4f}
    
    STATIONARITY RESULTS:
    --------------------
    Original Series Stationary: {stationarity_results['original_stationary']}
    First Difference Stationary: {stationarity_results['difference_stationary']}
    Returns Stationary: {stationarity_results['returns_stationary']}
    
    ARIMA MODEL PERFORMANCE:
    -----------------------
    Mean Absolute Error (MAE): {metrics['MAE']:.4f}
    Root Mean Squared Error (RMSE): {metrics['RMSE']:.4f}
    Mean Absolute Percentage Error (MAPE): {metrics['MAPE']:.2f}%
    
    KEY INSIGHTS:
    ------------
    1. The exchange rate shows significant volatility over time
    2. The series appears to be non-stationary, requiring differencing
    3. ARIMA model provides reasonable forecasts for short-term predictions
    4. Consider exploring additional models (SARIMA, Prophet) for improved accuracy
    
    RECOMMENDATIONS:
    ---------------
    - Monitor the model performance regularly
    - Consider external economic factors for improved forecasting
    - Retrain model with new data periodically
    - Explore ensemble methods for better accuracy
    """
    
    print(report)
    
    # Save report to file
    with open('results/analysis_report.txt', 'w') as f:
        f.write(report)

if __name__ == "__main__":
    # Create results directory if it doesn't exist
    import os
    if not os.path.exists('results'):
        os.makedirs('results')
    
    main()