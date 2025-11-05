"""
Advanced Time Series Analysis
Extended analysis including stationarity, autocorrelation, trend, seasonality
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class AdvancedTimeSeriesAnalyzer:
    """
    Advanced time series analysis with multiple modeling approaches
    """
    
    def __init__(self):
        self.data = None
        self.results = {}
        self.models = {}
        
    def load_data(self, filepath, date_column='date', value_column='rate'):
        """Load and prepare time series data"""
        try:
            self.data = pd.read_csv(filepath)
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            self.data = self.data.set_index(date_column)
            self.data = self.data[[value_column]].dropna()
            print(f"Data loaded: {len(self.data)} records")
            return self.data
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def comprehensive_analysis(self):
        """Perform comprehensive time series analysis"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        analysis_results = {}
        
        # Basic statistics
        analysis_results['basic_stats'] = {
            'mean': self.data.iloc[:, 0].mean(),
            'std': self.data.iloc[:, 0].std(),
            'min': self.data.iloc[:, 0].min(),
            'max': self.data.iloc[:, 0].max(),
            'count': len(self.data)
        }
        
        # Stationarity tests
        analysis_results['stationarity'] = self._stationarity_analysis()
        
        # Autocorrelation analysis
        analysis_results['autocorrelation'] = self._autocorrelation_analysis()
        
        # Trend and seasonality analysis
        analysis_results['decomposition'] = self._seasonal_decomposition()
        
        self.results['analysis'] = analysis_results
        return analysis_results
    
    def _stationarity_analysis(self):
        """Perform comprehensive stationarity analysis"""
        series = self.data.iloc[:, 0].dropna()
        
        # ADF Test
        adf_result = adfuller(series)
        adf_stationary = adf_result[1] <= 0.05
        
        # KPSS Test
        try:
            kpss_result = kpss(series, regression='c')
            kpss_stationary = kpss_result[1] >= 0.05
        except:
            kpss_stationary = False
            kpss_result = [None, None]
        
        return {
            'adf_statistic': adf_result[0],
            'adf_pvalue': adf_result[1],
            'adf_stationary': adf_stationary,
            'kpss_statistic': kpss_result[0],
            'kpss_pvalue': kpss_result[1],
            'kpss_stationary': kpss_stationary,
            'is_stationary': adf_stationary and kpss_stationary
        }
    
    def _autocorrelation_analysis(self):
        """Analyze autocorrelation and partial autocorrelation"""
        series = self.data.iloc[:, 0].dropna()
        
        # Calculate ACF and PACF
        acf_values = acf(series, nlags=40)
        pacf_values = pacf(series, nlags=40)
        
        # Find significant lags
        significant_acf = [i for i, val in enumerate(acf_values) if abs(val) > 1.96/np.sqrt(len(series))][1:6]
        significant_pacf = [i for i, val in enumerate(pacf_values) if abs(val) > 1.96/np.sqrt(len(series))][1:6]
        
        return {
            'acf_values': acf_values[:10].tolist(),
            'pacf_values': pacf_values[:10].tolist(),
            'significant_acf_lags': significant_acf,
            'significant_pacf_lags': significant_pacf
        }
    
    def _seasonal_decomposition(self):
        """Decompose time series into trend, seasonal, and residual components"""
        try:
            decomposition = seasonal_decompose(self.data.iloc[:, 0], model='additive', period=30)
            return {
                'trend_strength': np.std(decomposition.trend.dropna()) / np.std(decomposition.resid.dropna()),
                'seasonal_strength': np.std(decomposition.seasonal.dropna()) / np.std(decomposition.resid.dropna()),
                'has_seasonality': np.std(decomposition.seasonal.dropna()) > 0.1 * np.std(self.data.iloc[:, 0])
            }
        except:
            return {'error': 'Decomposition failed'}