"""
Time Series Analysis Module for Laboratory Work 4
Provides comprehensive time series analysis including stationarity tests and ARIMA modeling
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error


class TimeSeriesAnalyzer:
    """
    Comprehensive time series analysis toolkit
    Includes data loading, cleaning, visualization, and ARIMA modeling
    """
    
    def __init__(self):
        """Initialize the time series analyzer"""
        self.data = None
        self.model_fitted = None
        self.forecast = None
    
    def load_data(self, filepath, date_column='date', value_column='rate'):
        """
        Load time series data from CSV file
        
        Args:
            filepath (str): Path to CSV file
            date_column (str): Name of date column
            value_column (str): Name of value column
            
        Returns:
            pandas.DataFrame: Loaded and preprocessed data
        """
        try:
            # Read data from CSV file
            self.data = pd.read_csv(filepath)
            
            # Rename columns to standard format
            self.data.columns = [col.lower().replace(' ', '_') for col in self.data.columns]
            
            # Convert date column to datetime format
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            
            print("Data loaded successfully")
            print(f"First 5 rows:\n{self.data.head()}")
            print(f"\nData info:\n{self.data.info()}")
            print(f"\nBasic statistics:\n{self.data.describe()}")
            
            return self.data
            
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def clean_data(self):
        """
        Clean and preprocess the time series data
        Handles missing values and data anomalies
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        # Check for missing values
        print("Missing values:")
        print(self.data.isnull().sum())
        missing_rate = self.data.isnull().mean()
        print(f"Missing value rate: {missing_rate}")
        
        # Handle missing values if any
        if self.data.isnull().sum().sum() > 0:
            # Fill gaps using forward fill method
            self.data = self.data.fillna(method='ffill')
            print("Missing values filled using forward fill")
        else:
            print("No missing values found")
        
        # Check for data anomalies
        print(f"\nMinimum rate value: {self.data['rate'].min()}")
        print(f"Maximum rate value: {self.data['rate'].max()}")
        
        # Calculate median and mean
        median_rate = self.data['rate'].median()
        mean_rate = self.data['rate'].mean()
        
        print(f"Median rate: {median_rate}")
        print(f"Mean rate: {mean_rate}")
        
        # Add deviation columns
        self.data['deviation_from_median'] = self.data['rate'] - median_rate
        self.data['deviation_from_mean'] = self.data['rate'] - mean_rate
        self.data['abs_deviation_from_median'] = abs(self.data['rate'] - median_rate)
        self.data['abs_deviation_from_mean'] = abs(self.data['rate'] - mean_rate)
        
        print("\nData with added deviation columns:")
        print(self.data.head())
        
        return self.data
    
    def test_stationarity(self, timeseries_column='rate'):
        """
        Perform Augmented Dickey-Fuller test for stationarity
        
        Args:
            timeseries_column (str): Column name to test
            
        Returns:
            dict: Test results including ADF statistic and p-value
        """
        if self.data is None:
            raise ValueError("No data available for analysis")
        
        try:
            series = self.data[timeseries_column].dropna()
            result = adfuller(series)
            
            stationarity_result = {
                'adf_statistic': result[0],
                'p_value': result[1],
                'critical_values': result[4],
                'is_stationary': result[1] <= 0.05
            }
            
            print("Stationarity Test Results:")
            print(f"ADF Statistic: {result[0]:.6f}")
            print(f"p-value: {result[1]:.6f}")
            print("Critical Values:")
            for key, value in result[4].items():
                print(f"  {key}: {value:.6f}")
            print(f"Series is {'stationary' if result[1] <= 0.05 else 'not stationary'}")
            
            return stationarity_result
            
        except Exception as e:
            raise Exception(f"Stationarity test failed: {str(e)}")
    
    def fit_arima(self, data, order=(1,1,1), timeseries_column='rate'):
        """
        Fit ARIMA model to the time series
        
        Args:
            data (pandas.DataFrame): Time series data
            order (tuple): ARIMA order (p,d,q)
            timeseries_column (str): Column to model
            
        Returns:
            Fitted ARIMA model
        """
        try:
            series = data[timeseries_column].dropna()
            
            self.model = ARIMA(series, order=order)
            self.model_fitted = self.model.fit()
            
            print(f"ARIMA{order} model fitted successfully")
            print(f"Model AIC: {self.model_fitted.aic:.4f}")
            print(f"Model BIC: {self.model_fitted.bic:.4f}")
            
            return self.model_fitted
            
        except Exception as e:
            raise Exception(f"ARIMA model fitting failed: {str(e)}")
    
    def forecast_arima(self, steps=30):
        """
        Generate forecast using fitted ARIMA model
        
        Args:
            steps (int): Number of steps to forecast
            
        Returns:
            array: Forecast values
        """
        if self.model_fitted is None:
            raise ValueError("No fitted model available. Please fit ARIMA model first.")
        
        try:
            self.forecast = self.model_fitted.forecast(steps=steps)
            
            print(f"Generated {steps}-step forecast")
            print(f"Forecast values: {self.forecast}")
            
            return self.forecast
            
        except Exception as e:
            raise Exception(f"Forecast generation failed: {str(e)}")
    
    def detect_outliers_iqr(self, series):
        """
        Detect outliers using Interquartile Range (IQR) method
        
        Args:
            series (pandas.Series): Data series to analyze
            
        Returns:
            pandas.Series: Outlier values
        """
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        return outliers
    
    def generate_monthly_stats(self):
        """
        Generate monthly statistics for the time series
        
        Returns:
            pandas.DataFrame: Monthly statistics
        """
        if self.data is None:
            raise ValueError("No data available for analysis")
        
        self.data['year_month'] = self.data['date'].dt.to_period('M')
        monthly_stats = self.data.groupby('year_month').agg({
            'rate': ['mean', 'median', 'std', 'min', 'max']
        }).round(4)
        
        monthly_stats.columns = ['mean_rate', 'median_rate', 'std_rate', 'min_rate', 'max_rate']
        monthly_stats = monthly_stats.reset_index()
        
        # Calculate volatility
        monthly_stats['volatility'] = monthly_stats['std_rate'] / monthly_stats['mean_rate']
        
        print("Monthly statistics:")
        print(monthly_stats.head(10))
        
        return monthly_stats


# Utility functions for backward compatibility
def analyze_time_series(filepath):
    """
    Utility function to run complete time series analysis
    
    Args:
        filepath (str): Path to CSV file
        
    Returns:
        TimeSeriesAnalyzer: Analyzer object with results
    """
    analyzer = TimeSeriesAnalyzer()
    data = analyzer.load_data(filepath)
    analyzer.clean_data()
    analyzer.test_stationarity()
    analyzer.generate_monthly_stats()
    
    return analyzer


if __name__ == "__main__":
    """Test the time series analyzer"""
    try:
        analyzer = TimeSeriesAnalyzer()
        data = analyzer.load_data('dataset.csv')
        cleaned_data = analyzer.clean_data()
        stationarity = analyzer.test_stationarity()
        
        print("\nTime series analysis completed successfully")
        
    except Exception as e:
        print(f"Error in time series analysis: {e}")