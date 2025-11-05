"""
ARIMA model implementation for time series forecasting
Includes model training, validation, and forecasting
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

from config import VALUE_COLUMN, TEST_SIZE

class ARIMAModel:
    def __init__(self, data):
        self.data = data
        self.model = None
        self.model_fit = None
        self.forecast = None
        self.train_size = None
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """Setup consistent plotting style"""
        plt.style.use('seaborn-v0_8')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    def prepare_data(self, test_size=TEST_SIZE):
        """Split data into train and test sets"""
        self.train_size = int(len(self.data) * (1 - test_size))
        self.train_data = self.data[VALUE_COLUMN][:self.train_size]
        self.test_data = self.data[VALUE_COLUMN][self.train_size:]
        
        print(f"Training data: {len(self.train_data)} records")
        print(f"Test data: {len(self.test_data)} records")
        print(f"Training period: {self.train_data.index.min()} to {self.train_data.index.max()}")
        print(f"Test period: {self.test_data.index.min()} to {self.test_data.index.max()}")
    
    def find_best_arima(self, p_range=range(0, 3), d_range=range(0, 2), q_range=range(0, 3)):
        """Find best ARIMA parameters using AIC criterion"""
        best_aic = np.inf
        best_order = None
        best_model = None
        
        print("Searching for best ARIMA parameters...")
        
        for p in p_range:
            for d in d_range:
                for q in q_range:
                    try:
                        model = ARIMA(self.train_data, order=(p, d, q))
                        fitted_model = model.fit()
                        
                        if fitted_model.aic < best_aic:
                            best_aic = fitted_model.aic
                            best_order = (p, d, q)
                            best_model = fitted_model
                            
                        print(f"ARIMA({p},{d},{q}) - AIC: {fitted_model.aic:.2f}")
                        
                    except Exception as e:
                        continue
        
        print(f"\nBest model: ARIMA{best_order} with AIC: {best_aic:.2f}")
        return best_order, best_model
    
    def train_model(self, order=None):
        """Train ARIMA model with specified order or find best order"""
        if order is None:
            print("No order specified. Finding best ARIMA order...")
            best_order, self.model_fit = self.find_best_arima()
            self.order = best_order
        else:
            print(f"Training ARIMA{order} model...")
            self.order = order
            model = ARIMA(self.train_data, order=order)
            self.model_fit = model.fit()
        
        print("\nModel Summary:")
        print(self.model_fit.summary())
        
        return self.model_fit
    
    def validate_model(self, steps=None):
        """Validate model on test data"""
        if steps is None:
            steps = len(self.test_data)
        
        # Forecast on test data
        forecast = self.model_fit.forecast(steps=steps)
        self.forecast = pd.Series(forecast, index=self.test_data.index[:steps])
        
        # Calculate metrics
        actual = self.test_data[:steps]
        mse = mean_squared_error(actual, self.forecast)
        mae = mean_absolute_error(actual, self.forecast)
        rmse = np.sqrt(mse)
        
        metrics = {
            'MSE': mse,
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': np.mean(np.abs((actual - self.forecast) / actual)) * 100
        }
        
        print("\nValidation Metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")
        
        return metrics, self.forecast
    
    def plot_validation(self, save_path=None):
        """Plot validation results"""
        if self.forecast is None:
            print("No forecast available. Run validate_model first.")
            return
        
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # Full series with forecast
        axes[0].plot(self.train_data.index, self.train_data.values, 
                    label='Training Data', color=self.colors[0], linewidth=2)
        axes[0].plot(self.test_data.index, self.test_data.values, 
                    label='Actual Test Data', color=self.colors[1], linewidth=2)
        axes[0].plot(self.forecast.index, self.forecast.values, 
                    label='Forecast', color=self.colors[2], linewidth=2, linestyle='--')
        axes[0].set_title(f'ARIMA{self.order} Model: Training and Validation')
        axes[0].set_ylabel('Exchange Rate')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Zoom on test period
        axes[1].plot(self.test_data.index, self.test_data.values, 
                    label='Actual', color=self.colors[1], linewidth=2)
        axes[1].plot(self.forecast.index, self.forecast.values, 
                    label='Forecast', color=self.colors[2], linewidth=2, linestyle='--')
        axes[1].set_title('Validation Period Zoom')
        axes[1].set_ylabel('Exchange Rate')
        axes[1].set_xlabel('Date')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_residuals(self, save_path=None):
        """Plot model residuals"""
        if self.model_fit is None:
            print("No model fitted. Run train_model first.")
            return
        
        residuals = self.model_fit.resid
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Model Residuals Analysis', fontsize=16, fontweight='bold')
        
        # Residuals over time
        axes[0, 0].plot(residuals.index, residuals.values, color=self.colors[0])
        axes[0, 0].set_title('Residuals Over Time')
        axes[0, 0].set_ylabel('Residual')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Histogram of residuals
        axes[0, 1].hist(residuals, bins=50, alpha=0.7, color=self.colors[1], edgecolor='black')
        axes[0, 1].set_title('Distribution of Residuals')
        axes[0, 1].set_xlabel('Residual')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot')
        axes[1, 0].grid(True, alpha=0.3)
        
        # ACF of residuals
        from statsmodels.graphics.tsaplots import plot_acf
        plot_acf(residuals, ax=axes[1, 1], lags=40, alpha=0.05)
        axes[1, 1].set_title('ACF of Residuals')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        # Residual statistics
        print("\nResidual Statistics:")
        print(f"Mean: {residuals.mean():.6f}")
        print(f"Standard Deviation: {residuals.std():.6f}")
        print(f"Skewness: {residuals.skew():.6f}")
        print(f"Kurtosis: {residuals.kurtosis():.6f}")

# Example usage
if __name__ == "__main__":
    from data_loader import DataLoader
    
    loader = DataLoader()
    data = loader.load_data()
    
    if data is not None:
        # Prepare ARIMA model
        arima_model = ARIMAModel(data)
        arima_model.prepare_data()
        
        # Train model (automatically find best parameters)
        arima_model.train_model()
        
        # Validate model
        metrics, forecast = arima_model.validate_model()
        
        # Plot results
        arima_model.plot_validation('arima_validation.png')
        arima_model.plot_residuals('arima_residuals.png')