"""
Hyperparameter tuning
"""

import itertools
import pandas as pd
from AI.model_trainer import ModelTrainer

class HyperparameterTuner:
    """
    Tune hyperparameters for SARIMA and regression models
    """
    
    def __init__(self):
        self.best_params = {}
        self.tuning_results = []
        
    def tune_sarima(self, train_data, param_grid, seasonal_period=7):
        """Tune SARIMA hyperparameters"""
        best_score = float('inf')
        best_params = None
        
        # Generate all parameter combinations
        all_params = []
        for p, d, q in param_grid['order']:
            for P, D, Q, s in param_grid['seasonal_order']:
                all_params.append(((p, d, q), (P, D, Q, s)))
        
        print(f"Testing {len(all_params)} SARIMA parameter combinations...")
        
        for i, (order, seasonal_order) in enumerate(all_params):
            try:
                trainer = ModelTrainer()
                model = trainer.train_sarima(train_data, order, seasonal_order)
                
                if model is not None:
                    # Use AIC as evaluation metric
                    score = model.aic
                    
                    result = {
                        'order': order,
                        'seasonal_order': seasonal_order,
                        'aic': score,
                        'success': True
                    }
                    
                    if score < best_score:
                        best_score = score
                        best_params = (order, seasonal_order)
                    
                    self.tuning_results.append(result)
                    print(f"SARIMA {order} x {seasonal_order}: AIC = {score:.2f}")
                    
            except Exception as e:
                result = {
                    'order': order,
                    'seasonal_order': seasonal_order,
                    'error': str(e),
                    'success': False
                }
                self.tuning_results.append(result)
                print(f"SARIMA {order} x {seasonal_order}: Failed - {e}")
        
        self.best_params['sarima'] = {
            'order': best_params[0],
            'seasonal_order': best_params[1],
            'aic': best_score
        }
        
        return self.best_params['sarima']
    
    def tune_random_forest(self, X_train, y_train, param_grid):
        """Tune Random Forest hyperparameters"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_squared_error
        
        best_score = float('inf')
        best_params = None
        
        all_params = []
        for n_est in param_grid['n_estimators']:
            for depth in param_grid['max_depth']:
                for min_split in param_grid['min_samples_split']:
                    all_params.append((n_est, depth, min_split))
        
        print(f"Testing {len(all_params)} Random Forest parameter combinations...")
        
        for n_est, depth, min_split in all_params:
            try:
                model = RandomForestRegressor(
                    n_estimators=n_est,
                    max_depth=depth,
                    min_samples_split=min_split,
                    random_state=42
                )
                
                model.fit(X_train, y_train)
                predictions = model.predict(X_train)
                score = mean_squared_error(y_train, predictions)
                
                result = {
                    'n_estimators': n_est,
                    'max_depth': depth,
                    'min_samples_split': min_split,
                    'mse': score,
                    'success': True
                }
                
                if score < best_score:
                    best_score = score
                    best_params = (n_est, depth, min_split)
                
                self.tuning_results.append(result)
                print(f"RF n_est={n_est}, depth={depth}, min_split={min_split}: MSE = {score:.4f}")
                
            except Exception as e:
                result = {
                    'n_estimators': n_est,
                    'max_depth': depth,
                    'min_samples_split': min_split,
                    'error': str(e),
                    'success': False
                }
                self.tuning_results.append(result)
        
        self.best_params['random_forest'] = {
            'n_estimators': best_params[0],
            'max_depth': best_params[1],
            'min_samples_split': best_params[2],
            'mse': best_score
        }
        
        return self.best_params['random_forest']
    
    def save_tuning_results(self, filename):
        """Save hyperparameter tuning results to file"""
        df = pd.DataFrame(self.tuning_results)
        df.to_csv(filename, index=False)
        print(f"Tuning results saved to {filename}")