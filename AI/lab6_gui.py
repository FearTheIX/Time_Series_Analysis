"""
GUI for Laboratory Work 6 - Advanced Time Series Analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Add lab6 modules to path
sys.path.append('.')

from AI.advanced_analyzer import AdvancedTimeSeriesAnalyzer
from AI.model_trainer import ModelTrainer
from AI.hyperparameter_tuner import HyperparameterTuner

class Lab6GUI:
    """
    GUI for Laboratory Work 6 - Advanced Time Series Analysis and Modeling
    """
    
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.analyzer = AdvancedTimeSeriesAnalyzer()
        self.trainer = ModelTrainer()
        self.tuner = HyperparameterTuner()
        self.current_data = None
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the Lab 6 GUI interface"""
        # Main notebook for different sections
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Analysis Tab
        self.setup_analysis_tab()
        
        # Modeling Tab
        self.setup_modeling_tab()
        
        # Hyperparameter Tuning Tab
        self.setup_tuning_tab()
        
        # Model Evaluation Tab
        self.setup_evaluation_tab()
    
    def setup_analysis_tab(self):
        """Setup comprehensive analysis tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="1. Data Analysis")
        
        # Data loading
        load_frame = ttk.LabelFrame(analysis_frame, text="Data Loading")
        load_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(load_frame, text="Load Time Series Data", 
                  command=self.load_data).pack(padx=5, pady=5)
        
        self.data_info_label = ttk.Label(load_frame, text="No data loaded")
        self.data_info_label.pack(padx=5, pady=5)
        
        # Analysis controls
        analysis_controls = ttk.LabelFrame(analysis_frame, text="Analysis Controls")
        analysis_controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(analysis_controls, text="Run Comprehensive Analysis",
                  command=self.run_comprehensive_analysis).pack(padx=5, pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(analysis_frame, text="Analysis Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.analysis_text = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=scrollbar.set)
        
        self.analysis_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_modeling_tab(self):
        """Setup model training tab"""
        modeling_frame = ttk.Frame(self.notebook)
        self.notebook.add(modeling_frame, text="2. Model Training")
        
        # Model selection
        model_frame = ttk.LabelFrame(modeling_frame, text="Model Selection")
        model_frame.pack(fill='x', padx=10, pady=5)
        
        self.model_var = tk.StringVar(value="sarima")
        ttk.Radiobutton(model_frame, text="SARIMA", variable=self.model_var, 
                       value="sarima").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(model_frame, text="Linear Regression", variable=self.model_var, 
                       value="linear").pack(anchor='w', padx=5, pady=2)
        ttk.Radiobutton(model_frame, text="Random Forest", variable=self.model_var, 
                       value="random_forest").pack(anchor='w', padx=5, pady=2)
        
        # Training controls
        train_frame = ttk.LabelFrame(modeling_frame, text="Training Controls")
        train_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(train_frame, text="Prepare Data", 
                  command=self.prepare_data).pack(side='left', padx=5, pady=5)
        ttk.Button(train_frame, text="Train Selected Model", 
                  command=self.train_model).pack(side='left', padx=5, pady=5)
        ttk.Button(train_frame, text="Evaluate All Models", 
                  command=self.evaluate_models).pack(side='left', padx=5, pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(modeling_frame, text="Training Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.training_text = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.training_text.yview)
        self.training_text.configure(yscrollcommand=scrollbar.set)
        
        self.training_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_tuning_tab(self):
        """Setup hyperparameter tuning tab"""
        tuning_frame = ttk.Frame(self.notebook)
        self.notebook.add(tuning_frame, text="3. Hyperparameter Tuning")
        
        # Tuning controls
        controls_frame = ttk.LabelFrame(tuning_frame, text="Tuning Controls")
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Tune SARIMA Parameters",
                  command=self.tune_sarima).pack(side='left', padx=5, pady=5)
        ttk.Button(controls_frame, text="Tune Random Forest Parameters", 
                  command=self.tune_random_forest).pack(side='left', padx=5, pady=5)
        ttk.Button(controls_frame, text="Save Tuning Results",
                  command=self.save_tuning_results).pack(side='left', padx=5, pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(tuning_frame, text="Tuning Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tuning_text = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tuning_text.yview)
        self.tuning_text.configure(yscrollcommand=scrollbar.set)
        
        self.tuning_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_evaluation_tab(self):
        """Setup model evaluation and deployment tab"""
        eval_frame = ttk.Frame(self.notebook)
        self.notebook.add(eval_frame, text="4. Model Evaluation")
        
        # Model deployment
        deploy_frame = ttk.LabelFrame(eval_frame, text="Model Deployment")
        deploy_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(deploy_frame, text="Save Best Model",
                  command=self.save_best_model).pack(side='left', padx=5, pady=5)
        ttk.Button(deploy_frame, text="Load Model for Prediction",
                  command=self.load_model).pack(side='left', padx=5, pady=5)
        ttk.Button(deploy_frame, text="Generate Prediction Report",
                  command=self.generate_report).pack(side='left', padx=5, pady=5)
        
        # Prediction interface
        predict_frame = ttk.LabelFrame(eval_frame, text="Model Prediction")
        predict_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(predict_frame, text="Steps to forecast:").pack(side='left', padx=5, pady=5)
        self.forecast_steps = ttk.Entry(predict_frame, width=10)
        self.forecast_steps.pack(side='left', padx=5, pady=5)
        self.forecast_steps.insert(0, "30")
        
        ttk.Button(predict_frame, text="Make Prediction",
                  command=self.make_prediction).pack(side='left', padx=5, pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(eval_frame, text="Evaluation Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.evaluation_text = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.evaluation_text.yview)
        self.evaluation_text.configure(yscrollcommand=scrollbar.set)
        
        self.evaluation_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def load_data(self):
        """Load time series data"""
        filename = filedialog.askopenfilename(
            title="Select Time Series Data",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if filename:
            try:
                self.current_data = self.analyzer.load_data(filename)
                self.data_info_label.config(text=f"Loaded: {os.path.basename(filename)} - {len(self.current_data)} records")
                self.analysis_text.insert(tk.END, f"Data loaded successfully: {len(self.current_data)} records\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def run_comprehensive_analysis(self):
        """Run comprehensive time series analysis"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        try:
            self.analysis_text.delete(1.0, tk.END)
            self.analysis_text.insert(tk.END, "Running comprehensive analysis...\n")
            
            results = self.analyzer.comprehensive_analysis()
            
            # Display results
            self.analysis_text.insert(tk.END, "\n=== BASIC STATISTICS ===\n")
            for key, value in results['basic_stats'].items():
                self.analysis_text.insert(tk.END, f"{key}: {value}\n")
            
            self.analysis_text.insert(tk.END, "\n=== STATIONARITY ANALYSIS ===\n")
            stationarity = results['stationarity']
            self.analysis_text.insert(tk.END, f"ADF p-value: {stationarity['adf_pvalue']:.6f}\n")
            self.analysis_text.insert(tk.END, f"ADF Stationary: {stationarity['adf_stationary']}\n")
            self.analysis_text.insert(tk.END, f"KPSS Stationary: {stationarity['kpss_stationary']}\n")
            self.analysis_text.insert(tk.END, f"Overall Stationary: {stationarity['is_stationary']}\n")
            
            self.analysis_text.insert(tk.END, "\n=== AUTOCORRELATION ANALYSIS ===\n")
            acf_info = results['autocorrelation']
            self.analysis_text.insert(tk.END, f"Significant ACF lags: {acf_info['significant_acf_lags']}\n")
            self.analysis_text.insert(tk.END, f"Significant PACF lags: {acf_info['significant_pacf_lags']}\n")
            
            self.analysis_text.insert(tk.END, "\nAnalysis completed successfully!\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
    
    def prepare_data(self):
        """Prepare data for modeling"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        try:
            self.training_text.insert(tk.END, "Preparing data for modeling...\n")
            
            # Prepare data for both ARIMA and regression
            self.arima_train, self.arima_test = self.trainer.prepare_arima_data(self.current_data)
            self.X_train, self.X_test, self.y_train, self.y_test = self.trainer.prepare_regression_data(self.current_data)
            
            self.training_text.insert(tk.END, f"ARIMA - Train: {len(self.arima_train)}, Test: {len(self.arima_test)}\n")
            self.training_text.insert(tk.END, f"Regression - X_train: {len(self.X_train)}, X_test: {len(self.X_test)}\n")
            self.training_text.insert(tk.END, "Data preparation completed!\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Data preparation failed: {str(e)}")
    
    def train_model(self):
        """Train selected model"""
        if not hasattr(self, 'arima_train'):
            messagebox.showwarning("Warning", "Please prepare data first")
            return
        
        model_type = self.model_var.get()
        
        try:
            self.training_text.insert(tk.END, f"Training {model_type} model...\n")
            
            if model_type == "sarima":
                model = self.trainer.train_sarima(self.arima_train)
                if model:
                    self.training_text.insert(tk.END, f"SARIMA model trained successfully. AIC: {model.aic:.2f}\n")
                else:
                    self.training_text.insert(tk.END, "SARIMA training failed\n")
            
            elif model_type in ["linear", "random_forest"]:
                models = self.trainer.train_regression_models(self.X_train, self.y_train)
                if model_type in models:
                    self.training_text.insert(tk.END, f"{model_type} model trained successfully\n")
                else:
                    self.training_text.insert(tk.END, f"{model_type} training failed\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Model training failed: {str(e)}")
    
    def evaluate_models(self):
        """Evaluate all trained models"""
        if not hasattr(self, 'arima_test'):
            messagebox.showwarning("Warning", "Please prepare data first")
            return
        
        try:
            self.training_text.insert(tk.END, "Evaluating all models...\n")
            
            results = self.trainer.evaluate_models(
                self.arima_test, self.X_test, self.y_test
            )
            
            self.training_text.insert(tk.END, "\n=== MODEL EVALUATION RESULTS ===\n")
            for model_name, metrics in results.items():
                self.training_text.insert(tk.END, f"\n{model_name.upper()}:\n")
                if 'error' in metrics:
                    self.training_text.insert(tk.END, f"  Error: {metrics['error']}\n")
                else:
                    for metric, value in metrics.items():
                        self.training_text.insert(tk.END, f"  {metric}: {value:.4f}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Model evaluation failed: {str(e)}")
    
    def tune_sarima(self):
        """Tune SARIMA hyperparameters"""
        if not hasattr(self, 'arima_train'):
            messagebox.showwarning("Warning", "Please prepare data first")
            return
        
        try:
            self.tuning_text.insert(tk.END, "Starting SARIMA hyperparameter tuning...\n")
            
            # Define parameter grid
            param_grid = {
                'order': [(1,1,1), (1,1,2), (2,1,1), (2,1,2)],
                'seasonal_order': [(1,1,1,7), (1,1,1,30), (0,1,1,7), (1,0,1,7)]
            }
            
            best_params = self.tuner.tune_sarima(self.arima_train, param_grid)
            
            self.tuning_text.insert(tk.END, "\n=== BEST SARIMA PARAMETERS ===\n")
            self.tuning_text.insert(tk.END, f"Order: {best_params['order']}\n")
            self.tuning_text.insert(tk.END, f"Seasonal Order: {best_params['seasonal_order']}\n")
            self.tuning_text.insert(tk.END, f"AIC: {best_params['aic']:.2f}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"SARIMA tuning failed: {str(e)}")
    
    def tune_random_forest(self):
        """Tune Random Forest hyperparameters"""
        if not hasattr(self, 'X_train'):
            messagebox.showwarning("Warning", "Please prepare data first")
            return
        
        try:
            self.tuning_text.insert(tk.END, "Starting Random Forest hyperparameter tuning...\n")
            
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, None],
                'min_samples_split': [2, 5, 10]
            }
            
            best_params = self.tuner.tune_random_forest(self.X_train, self.y_train, param_grid)
            
            self.tuning_text.insert(tk.END, "\n=== BEST RANDOM FOREST PARAMETERS ===\n")
            for param, value in best_params.items():
                if param != 'mse':
                    self.tuning_text.insert(tk.END, f"{param}: {value}\n")
            self.tuning_text.insert(tk.END, f"MSE: {best_params['mse']:.4f}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Random Forest tuning failed: {str(e)}")
    
    def save_tuning_results(self):
        """Save hyperparameter tuning results"""
        filename = filedialog.asksaveasfilename(
            title="Save Tuning Results",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if filename:
            self.tuner.save_tuning_results(filename)
            self.tuning_text.insert(tk.END, f"Tuning results saved to: {filename}\n")
    
    def save_best_model(self):
        """Save the best performing model"""
        # Implementation for saving models
        self.evaluation_text.insert(tk.END, "Model saving functionality - to be implemented\n")
    
    def load_model(self):
        """Load a saved model"""
        # Implementation for loading models
        self.evaluation_text.insert(tk.END, "Model loading functionality - to be implemented\n")
    
    def generate_report(self):
        """Generate comprehensive report"""
        # Implementation for report generation
        self.evaluation_text.insert(tk.END, "Report generation functionality - to be implemented\n")
    
    def make_prediction(self):
        """Make predictions using trained models"""
        # Implementation for predictions
        self.evaluation_text.insert(tk.END, "Prediction functionality - to be implemented\n")