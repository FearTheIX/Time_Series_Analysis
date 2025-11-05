"""
Model training
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    """
    Train and compare SARIMA and regression models
    """
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def prepare_arima_data(self, data, test_size=0.2):
        """Prepare data for ARIMA models"""
        series = data.iloc[:, 0]
        split_idx = int(len(series) * (1 - test_size))
        
        train_data = series[:split_idx]
        test_data = series[split_idx:]
        
        return train_data, test_data
    
    def prepare_regression_data(self, data, n_lags=5, test_size=0.2):
        """Prepare data for regression models with lag features"""
        df = data.copy()
        
        # Create lag features
        for lag in range(1, n_lags + 1):
            df[f'lag_{lag}'] = df.iloc[:, 0].shift(lag)
        
        # Create rolling statistics
        df['rolling_mean_3'] = df.iloc[:, 0].rolling(window=3).mean()
        df['rolling_std_3'] = df.iloc[:, 0].rolling(window=3).std()
        
        # Drop NaN values
        df = df.dropna()
        
        # Prepare features and target
        X = df.drop(columns=[df.columns[0]])
        y = df.iloc[:, 0]
        
        # Split data
        split_idx = int(len(X) * (1 - test_size))
        
        X_train = X[:split_idx]
        X_test = X[split_idx:]
        y_train = y[:split_idx]
        y_test = y[split_idx:]
        
        return X_train, X_test, y_train, y_test
    
    def train_sarima(self, train_data, order=(1,1,1), seasonal_order=(1,1,1,7)):
        """Train SARIMA model"""
        try:
            model = SARIMAX(train_data, 
                          order=order, 
                          seasonal_order=seasonal_order,
                          enforce_stationarity=False,
                          enforce_invertibility=False)
            
            fitted_model = model.fit(disp=False)
            self.models['sarima'] = fitted_model
            return fitted_model
        except Exception as e:
            print(f"SARIMA training failed: {e}")
            return None
    
    def train_regression_models(self, X_train, y_train):
        """Train multiple regression models"""
        models = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        for name, model in models.items():
            try:
                model.fit(X_train, y_train)
                self.models[name] = model
                print(f"Trained {name} successfully")
            except Exception as e:
                print(f"Failed to train {name}: {e}")
        
        return self.models
    
    def evaluate_models(self, test_data, X_test=None, y_test=None):
        """Evaluate all trained models"""
        evaluation_results = {}
        
        # Evaluate SARIMA
        if 'sarima' in self.models:
            try:
                forecast = self.models['sarima'].forecast(steps=len(test_data))
                sarima_metrics = self._calculate_metrics(test_data.values, forecast)
                evaluation_results['sarima'] = sarima_metrics
            except Exception as e:
                evaluation_results['sarima'] = {'error': str(e)}
        
        # Evaluate regression models
        if X_test is not None and y_test is not None:
            for name, model in self.models.items():
                if name != 'sarima':
                    try:
                        predictions = model.predict(X_test)
                        metrics = self._calculate_metrics(y_test.values, predictions)
                        evaluation_results[name] = metrics
                    except Exception as e:
                        evaluation_results[name] = {'error': str(e)}
        
        self.results['evaluation'] = evaluation_results
        return evaluation_results
    
    def _calculate_metrics(self, actual, predicted):
        """Calculate evaluation metrics"""
        return {
            'mse': mean_squared_error(actual, predicted),
            'mae': mean_absolute_error(actual, predicted),
            'rmse': np.sqrt(mean_squared_error(actual, predicted)),
            'mape': np.mean(np.abs((actual - predicted) / actual)) * 100
        }