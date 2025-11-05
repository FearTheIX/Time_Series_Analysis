"""
Stationarity analysis and time series decomposition
Includes ADF test and seasonal decomposition
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from config import VALUE_COLUMN

class StationarityAnalysis:
    def __init__(self, data):
        self.data = data
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """Setup consistent plotting style"""
        plt.style.use('seaborn-v0_8')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    def adf_test(self, series):
        """Perform Augmented Dickey-Fuller test for stationarity"""
        result = adfuller(series.dropna())
        
        adf_statistic = result[0]
        p_value = result[1]
        critical_values = result[4]
        
        print('=== Augmented Dickey-Fuller Test ===')
        print(f'ADF Statistic: {adf_statistic:.6f}')
        print(f'p-value: {p_value:.6f}')
        print('Critical Values:')
        for key, value in critical_values.items():
            print(f'   {key}: {value:.3f}')
        
        if p_value < 0.05:
            print("Result: Series is stationary (reject null hypothesis)")
            return True
        else:
            print("Result: Series is non-stationary (cannot reject null hypothesis)")
            return False
    
    def plot_acf_pacf(self, series, lags=40, save_path=None):
        """Plot ACF and PACF for the series"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # ACF plot
        plot_acf(series, ax=ax1, lags=lags, alpha=0.05)
        ax1.set_title('Autocorrelation Function (ACF)')
        ax1.grid(True, alpha=0.3)
        
        # PACF plot
        plot_pacf(series, ax=ax2, lags=lags, alpha=0.05, method='ywm')
        ax2.set_title('Partial Autocorrelation Function (PACF)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def seasonal_decomposition(self, period=252, save_path=None):
        """Perform seasonal decomposition of time series"""
        try:
            # Ensure we have enough data points
            if len(self.data) < period * 2:
                print(f"Warning: Not enough data for {period}-period decomposition")
                period = min(period, len(self.data) // 2)
            
            decomposition = seasonal_decompose(self.data[VALUE_COLUMN], 
                                            model='additive', period=period)
            
            fig, axes = plt.subplots(4, 1, figsize=(15, 12))
            fig.suptitle('Time Series Decomposition', fontsize=16, fontweight='bold')
            
            # Original series
            axes[0].plot(decomposition.observed, color=self.colors[0])
            axes[0].set_ylabel('Observed')
            axes[0].grid(True, alpha=0.3)
            
            # Trend component
            axes[1].plot(decomposition.trend, color=self.colors[1])
            axes[1].set_ylabel('Trend')
            axes[1].grid(True, alpha=0.3)
            
            # Seasonal component
            axes[2].plot(decomposition.seasonal, color=self.colors[2])
            axes[2].set_ylabel('Seasonal')
            axes[2].grid(True, alpha=0.3)
            
            # Residual component
            axes[3].plot(decomposition.resid, color=self.colors[3])
            axes[3].set_ylabel('Residual')
            axes[3].set_xlabel('Date')
            axes[3].grid(True, alpha=0.3)
            
            plt.tight_layout()
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            return decomposition
            
        except Exception as e:
            print(f"Error in seasonal decomposition: {str(e)}")
            return None
    
    def analyze_stationarity(self):
        """Complete stationarity analysis"""
        print("=== STATIONARITY ANALYSIS ===")
        
        # Test original series
        print("\n1. Original Series:")
        is_stationary_original = self.adf_test(self.data[VALUE_COLUMN])
        
        # Test first difference
        print("\n2. First Difference:")
        first_diff = self.data[VALUE_COLUMN].diff().dropna()
        is_stationary_diff = self.adf_test(first_diff)
        
        # Test returns (percentage change)
        print("\n3. Percentage Returns:")
        returns = self.data[VALUE_COLUMN].pct_change().dropna()
        is_stationary_returns = self.adf_test(returns)
        
        # Plot all series
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Original series
        axes[0, 0].plot(self.data.index, self.data[VALUE_COLUMN])
        axes[0, 0].set_title('Original Series')
        axes[0, 0].set_ylabel('Exchange Rate')
        axes[0, 0].grid(True, alpha=0.3)
        
        # First difference
        axes[0, 1].plot(first_diff.index, first_diff)
        axes[0, 1].set_title('First Difference')
        axes[0, 1].set_ylabel('Difference')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Returns
        axes[1, 0].plot(returns.index, returns)
        axes[1, 0].set_title('Percentage Returns')
        axes[1, 0].set_ylabel('Return')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Histogram of returns
        axes[1, 1].hist(returns, bins=50, alpha=0.7, edgecolor='black')
        axes[1, 1].set_title('Distribution of Returns')
        axes[1, 1].set_xlabel('Return')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return {
            'original_stationary': is_stationary_original,
            'difference_stationary': is_stationary_diff,
            'returns_stationary': is_stationary_returns,
            'first_difference': first_diff,
            'returns': returns
        }

# Example usage
if __name__ == "__main__":
    from data_loader import DataLoader
    
    loader = DataLoader()
    data = loader.load_data()
    
    if data is not None:
        analyzer = StationarityAnalysis(data)
        
        # Perform stationarity analysis
        stationarity_results = analyzer.analyze_stationarity()
        
        # Plot ACF and PACF
        analyzer.plot_acf_pacf(data[VALUE_COLUMN], save_path='acf_pacf.png')
        
        # Seasonal decomposition
        decomposition = analyzer.seasonal_decomposition(save_path='decomposition.png')