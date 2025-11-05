"""
Integrated Analytics Platform using Tkinter
Combining all laboratory works: Web Scraping, Data Processing, Time Series Analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import datetime
import pandas as pd

# Import modules from different labs - GLOBAL SCOPE
try:
    from currency_scrapper_v2 import CurrencyScraper
    SCRAPER_AVAILABLE = True
except ImportError as e:
    SCRAPER_AVAILABLE = False
    print(f"Warning: Lab 1 module not found: {e}")

try:
    from data_processor import CurrencyDataProcessor, get_rate_single_file, get_rate_x_y, get_rate_year_files, get_rate_week_files
    from annotation_creator import create_annotation_file, create_reorganized_dataset
    LAB3_AVAILABLE = True
except ImportError as e:
    LAB3_AVAILABLE = False
    print(f"Warning: Lab 3 modules not found: {e}")

try:
    from time_series_analyzer import TimeSeriesAnalyzer
    LAB4_AVAILABLE = True
except ImportError as e:
    LAB4_AVAILABLE = False
    print(f"Warning: Lab 4 module not found: {e}")

# Try to import Lab 6 modules
try:
    from AI.advanced_analyzer import AdvancedTimeSeriesAnalyzer
    from AI.model_trainer import ModelTrainer
    from AI.hyperparameter_tuner import HyperparameterTuner
    LAB6_AVAILABLE = True
except ImportError as e:
    LAB6_AVAILABLE = False
    print(f"Warning: Lab 6 modules not found: {e}")


class IntegratedAnalyticsPlatform:
    """
    Main integrated GUI window using Tkinter
    """
    
    def __init__(self, root):
        """Initialize the main window with all laboratory features"""
        self.root = root
        self.root.title("Integrated Analytics Platform - All Labs")
        self.root.geometry("1000x800")
        
        self.dataset_path = ""
        self.current_data = None
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface with tabs for each lab"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs for each laboratory
        if SCRAPER_AVAILABLE:
            self.setup_lab1_tab()
        
        if LAB3_AVAILABLE:
            self.setup_lab3_tab()
            
        if LAB4_AVAILABLE:
            self.setup_lab4_tab()
        
        # Add Lab 6 tab if available
        if LAB6_AVAILABLE:
            self.setup_lab6_tab()
        
        # Add testing tab
        self.setup_testing_tab()
        
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.log("Application started successfully")
        self.update_module_status()
    
    def setup_lab1_tab(self):
        """Setup Lab 1: Web Scraping tab"""
        lab1_frame = ttk.Frame(self.notebook)
        self.notebook.add(lab1_frame, text="Lab 1: Web Scraping")
        
        # Web scraping section
        scraping_group = ttk.LabelFrame(lab1_frame, text="Web Scraping (Lab 1) - Central Bank of Russia")
        scraping_group.pack(fill='x', padx=10, pady=5)
        
        # Replace URL field with year field
        ttk.Label(scraping_group, text="Start Year:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.start_year_entry = ttk.Entry(scraping_group, width=10)
        self.start_year_entry.grid(row=0, column=1, padx=5, pady=5)
        self.start_year_entry.insert(0, "2020")  # Default year
        
        self.scrape_btn = ttk.Button(scraping_group, text="Start Scraping", command=self.start_web_scraping)
        self.scrape_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Results display
        ttk.Label(lab1_frame, text="Scraping Results:").pack(anchor='w', padx=10, pady=(10,0))
        
        results_frame = tk.Frame(lab1_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.scraping_results = tk.Text(results_frame, height=15, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.scraping_results.yview)
        self.scraping_results.configure(yscrollcommand=scrollbar.set)
        
        self.scraping_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_lab3_tab(self):
        """Setup Lab 3: Data Processing tab"""
        lab3_frame = ttk.Frame(self.notebook)
        self.notebook.add(lab3_frame, text="Lab 3: Data Processing")
        
        # Dataset selection
        dataset_group = ttk.LabelFrame(lab3_frame, text="Dataset Selection")
        dataset_group.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(dataset_group, text="Dataset:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.dataset_path_label = ttk.Label(dataset_group, text="No dataset selected")
        self.dataset_path_label.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        self.select_dataset_btn = ttk.Button(dataset_group, text="Select Dataset Folder", command=self.select_dataset_folder)
        self.select_dataset_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Data processing buttons
        processing_group = ttk.LabelFrame(lab3_frame, text="Data Processing")
        processing_group.pack(fill='x', padx=10, pady=5)
        
        self.create_annotation_btn = ttk.Button(processing_group, text="Create Annotation File", command=self.create_annotation)
        self.create_annotation_btn.pack(padx=5, pady=2)
        
        self.split_xy_btn = ttk.Button(processing_group, text="Split to X and Y Files", command=self.split_to_xy)
        self.split_xy_btn.pack(padx=5, pady=2)
        
        self.split_yearly_btn = ttk.Button(processing_group, text="Split by Years", command=self.split_by_years)
        self.split_yearly_btn.pack(padx=5, pady=2)
        
        self.split_weekly_btn = ttk.Button(processing_group, text="Split by Weeks", command=self.split_by_weeks)
        self.split_weekly_btn.pack(padx=5, pady=2)
        
        # Date search section
        search_group = ttk.LabelFrame(lab3_frame, text="Date Search")
        search_group.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_group, text="Date:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.date_input = ttk.Entry(search_group, width=15)
        self.date_input.grid(row=0, column=1, padx=5, pady=5)
        self.date_input.insert(0, "YYYY-MM-DD")
        
        ttk.Label(search_group, text="Method:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.search_method_combo = ttk.Combobox(search_group, values=["Single File", "X/Y Files", "Yearly Files", "Weekly Files"])
        self.search_method_combo.set("Single File")
        self.search_method_combo.grid(row=0, column=3, padx=5, pady=5)
        
        self.search_btn = ttk.Button(search_group, text="Search Date", command=self.search_date)
        self.search_btn.grid(row=0, column=4, padx=5, pady=5)
        
        ttk.Label(search_group, text="Result:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.search_result = tk.Text(search_group, height=3, width=80)
        self.search_result.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky='we')
        
        # Log display
        ttk.Label(lab3_frame, text="Processing Log:").pack(anchor='w', padx=10, pady=(10,0))
        
        log_frame = tk.Frame(lab3_frame)
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lab3_log = tk.Text(log_frame, height=10, width=100)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.lab3_log.yview)
        self.lab3_log.configure(yscrollcommand=scrollbar.set)
        
        self.lab3_log.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_lab4_tab(self):
        """Setup Lab 4: Time Series Analysis tab"""
        lab4_frame = ttk.Frame(self.notebook)
        self.notebook.add(lab4_frame, text="Lab 4: Time Series")
        
        # Data loading section
        load_group = ttk.LabelFrame(lab4_frame, text="Data Loading")
        load_layout = ttk.Frame(load_group)
        load_layout.pack(fill='x', padx=5, pady=5)
        
        self.load_data_btn = ttk.Button(load_layout, text="Load Time Series Data", command=self.load_timeseries_data)
        self.load_data_btn.pack(side='left', padx=5, pady=5)
        
        self.data_info_label = ttk.Label(load_layout, text="No data loaded")
        self.data_info_label.pack(side='left', padx=5, pady=5)
        
        load_group.pack(fill='x', padx=10, pady=5)
        
        # Analysis controls
        analysis_group = ttk.LabelFrame(lab4_frame, text="Time Series Analysis")
        analysis_layout = ttk.Frame(analysis_group)
        analysis_layout.pack(fill='x', padx=5, pady=5)
        
        self.stationarity_btn = ttk.Button(analysis_layout, text="Stationarity Analysis", command=self.analyze_stationarity)
        self.stationarity_btn.pack(side='left', padx=5, pady=5)
        
        self.build_arima_btn = ttk.Button(analysis_layout, text="Build ARIMA Model", command=self.build_arima_model)
        self.build_arima_btn.pack(side='left', padx=5, pady=5)
        
        self.forecast_btn = ttk.Button(analysis_layout, text="Generate Forecast", command=self.generate_forecast)
        self.forecast_btn.pack(side='left', padx=5, pady=5)
        
        analysis_group.pack(fill='x', padx=10, pady=5)
        
        # Results display
        ttk.Label(lab4_frame, text="Analysis Results:").pack(anchor='w', padx=10, pady=(10,0))
        
        results_frame = tk.Frame(lab4_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lab4_results = tk.Text(results_frame, height=15, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab4_results.yview)
        self.lab4_results.configure(yscrollcommand=scrollbar.set)
        
        self.lab4_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_lab6_tab(self):
        """Setup Lab 6: Advanced Time Series Analysis with full functionality"""
        if not LAB6_AVAILABLE:
            lab6_frame = ttk.Frame(self.notebook)
            self.notebook.add(lab6_frame, text="Lab 6: Advanced Analysis")
            ttk.Label(lab6_frame, text="Lab 6 modules not available").pack(pady=20)
            return
    
        lab6_frame = ttk.Frame(self.notebook)
        self.notebook.add(lab6_frame, text="Lab 6: Advanced Analysis")
    
        # Create notebook for Lab 6 sections
        lab6_notebook = ttk.Notebook(lab6_frame)
        lab6_notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
        # Tab 1: Data Analysis
        analysis_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(analysis_tab, text="1. Data Analysis")
        self.setup_lab6_analysis_tab(analysis_tab)
    
        # Tab 2: Model Training
        training_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(training_tab, text="2. Model Training")
        self.setup_lab6_training_tab(training_tab)
    
        # Tab 3: Hyperparameter Tuning
        tuning_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(tuning_tab, text="3. Hyperparameter Tuning")
        self.setup_lab6_tuning_tab(tuning_tab)

        # Tab 4: Model Evaluation
        eval_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(eval_tab, text="4. Model Evaluation")
        self.setup_lab6_evaluation_tab(eval_tab)

    def setup_lab6_analysis_tab(self, parent):
        """Setup Lab 6 Data Analysis tab"""
        # Data loading section
        load_frame = ttk.LabelFrame(parent, text="Data Loading")
        load_frame.pack(fill='x', padx=10, pady=5)
    
        ttk.Button(load_frame, text="Load Dataset for Analysis", 
              command=self.load_lab6_data).pack(padx=5, pady=5)
    
        self.lab6_data_info = ttk.Label(load_frame, text="No data loaded")
        self.lab6_data_info.pack(padx=5, pady=5)
    
        # Analysis controls
        analysis_frame = ttk.LabelFrame(parent, text="Advanced Analysis")
        analysis_frame.pack(fill='x', padx=10, pady=5)
    
        analysis_buttons = ttk.Frame(analysis_frame)
        analysis_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(analysis_buttons, text="Comprehensive Analysis",
              command=self.run_lab6_analysis).pack(side='left', padx=5, pady=5)
        ttk.Button(analysis_buttons, text="Stationarity Tests",
              command=self.run_stationarity_tests).pack(side='left', padx=5, pady=5)
        ttk.Button(analysis_buttons, text="Autocorrelation Analysis",
              command=self.run_autocorrelation_analysis).pack(side='left', padx=5, pady=5)
        ttk.Button(analysis_buttons, text="Seasonal Decomposition",
              command=self.run_seasonal_decomposition).pack(side='left', padx=5, pady=5)
    
        # Results display
        results_frame = ttk.LabelFrame(parent, text="Analysis Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_analysis_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_analysis_results.yview)
        self.lab6_analysis_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_analysis_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_lab6_training_tab(self, parent):
        """Setup Lab 6 Model Training tab"""
        # Data preparation
        prep_frame = ttk.LabelFrame(parent, text="Data Preparation")
        prep_frame.pack(fill='x', padx=10, pady=5)
    
        ttk.Button(prep_frame, text="Prepare Data for Modeling",
              command=self.prepare_lab6_data).pack(padx=5, pady=5)
    
        self.lab6_prep_info = ttk.Label(prep_frame, text="Data not prepared")
        self.lab6_prep_info.pack(padx=5, pady=5)
    
        # Model selection
        model_frame = ttk.LabelFrame(parent, text="Model Selection")
        model_frame.pack(fill='x', padx=10, pady=5)
    
        model_buttons = ttk.Frame(model_frame)
        model_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(model_buttons, text="Train SARIMA Model",
              command=self.train_sarima_model).pack(side='left', padx=5, pady=5)
        ttk.Button(model_buttons, text="Train Linear Regression",
              command=self.train_linear_model).pack(side='left', padx=5, pady=5)
        ttk.Button(model_buttons, text="Train Random Forest",
              command=self.train_random_forest).pack(side='left', padx=5, pady=5)
        ttk.Button(model_buttons, text="Evaluate All Models",
              command=self.evaluate_lab6_models).pack(side='left', padx=5, pady=5)
    
        # Training results
        results_frame = ttk.LabelFrame(parent, text="Training Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_training_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_training_results.yview)
        self.lab6_training_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_training_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_lab6_tuning_tab(self, parent):
        """Setup Lab 6 Hyperparameter Tuning tab"""
        # Tuning controls
        tuning_frame = ttk.LabelFrame(parent, text="Hyperparameter Tuning")
        tuning_frame.pack(fill='x', padx=10, pady=5)
    
        tuning_buttons = ttk.Frame(tuning_frame)
        tuning_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(tuning_buttons, text="Tune SARIMA Parameters",
              command=self.tune_sarima_params).pack(side='left', padx=5, pady=5)
        ttk.Button(tuning_buttons, text="Tune Random Forest Parameters",
              command=self.tune_rf_params).pack(side='left', padx=5, pady=5)
        ttk.Button(tuning_buttons, text="Save Tuning Results",
              command=self.save_tuning_results).pack(side='left', padx=5, pady=5)
    
        # Parameter configuration
        param_frame = ttk.LabelFrame(parent, text="Parameter Configuration")
        param_frame.pack(fill='x', padx=10, pady=5)
    
        # SARIMA parameters
        sarima_frame = ttk.Frame(param_frame)
        sarima_frame.pack(fill='x', padx=5, pady=5)
    
        ttk.Label(sarima_frame, text="SARIMA Order (p,d,q):").grid(row=0, column=0, sticky='w', padx=5)
        self.sarima_order = ttk.Entry(sarima_frame, width=15)
        self.sarima_order.grid(row=0, column=1, padx=5)
        self.sarima_order.insert(0, "1,1,1")
    
        ttk.Label(sarima_frame, text="Seasonal Order (P,D,Q,s):").grid(row=0, column=2, sticky='w', padx=5)
        self.seasonal_order = ttk.Entry(sarima_frame, width=15)
        self.seasonal_order.grid(row=0, column=3, padx=5)
        self.seasonal_order.insert(0, "1,1,1,7")
    
        # Random Forest parameters
        rf_frame = ttk.Frame(param_frame)
        rf_frame.pack(fill='x', padx=5, pady=5)
    
        ttk.Label(rf_frame, text="n_estimators:").grid(row=0, column=0, sticky='w', padx=5)
        self.n_estimators = ttk.Entry(rf_frame, width=10)
        self.n_estimators.grid(row=0, column=1, padx=5)
        self.n_estimators.insert(0, "100")
    
        ttk.Label(rf_frame, text="max_depth:").grid(row=0, column=2, sticky='w', padx=5)
        self.max_depth = ttk.Entry(rf_frame, width=10)
        self.max_depth.grid(row=0, column=3, padx=5)
        self.max_depth.insert(0, "10")
    
        # Tuning results
        results_frame = ttk.LabelFrame(parent, text="Tuning Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_tuning_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_tuning_results.yview)
        self.lab6_tuning_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_tuning_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_lab6_evaluation_tab(self, parent):
        """Setup Lab 6 Model Evaluation tab"""
        # Model deployment
        deploy_frame = ttk.LabelFrame(parent, text="Model Deployment")
        deploy_frame.pack(fill='x', padx=10, pady=5)
    
        deploy_buttons = ttk.Frame(deploy_frame)
        deploy_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(deploy_buttons, text="Save Best Model",
              command=self.save_best_model).pack(side='left', padx=5, pady=5)
        ttk.Button(deploy_buttons, text="Load Saved Model",
              command=self.load_saved_model).pack(side='left', padx=5, pady=5)
        ttk.Button(deploy_buttons, text="Generate Report",
              command=self.generate_lab6_report).pack(side='left', padx=5, pady=5)
    
        # Prediction interface
        predict_frame = ttk.LabelFrame(parent, text="Model Prediction")
        predict_frame.pack(fill='x', padx=10, pady=5)
    
        predict_controls = ttk.Frame(predict_frame)
        predict_controls.pack(fill='x', padx=5, pady=5)
    
        ttk.Label(predict_controls, text="Forecast Steps:").pack(side='left', padx=5)
        self.forecast_steps_entry = ttk.Entry(predict_controls, width=10)
        self.forecast_steps_entry.pack(side='left', padx=5)
        self.forecast_steps_entry.insert(0, "30")
    
        ttk.Button(predict_controls, text="Make Prediction",
              command=self.make_lab6_prediction).pack(side='left', padx=5)
    
        ttk.Label(predict_controls, text="Model:").pack(side='left', padx=5)
        self.model_selector = ttk.Combobox(predict_controls, 
                                     values=["SARIMA", "Linear Regression", "Random Forest"])
        self.model_selector.set("SARIMA")
        self.model_selector.pack(side='left', padx=5)
    
        # Evaluation results
        results_frame = ttk.LabelFrame(parent, text="Evaluation Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_evaluation_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_evaluation_results.yview)
        self.lab6_evaluation_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_evaluation_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_testing_tab(self):
        """Setup testing and diagnostics tab"""
        test_frame = ttk.Frame(self.notebook)
        self.notebook.add(test_frame, text="Testing & Diagnostics")
        
        # Module status
        status_group = ttk.LabelFrame(test_frame, text="Module Status")
        status_group.pack(fill='x', padx=10, pady=5)
        
        self.status_display = tk.Text(status_group, height=6, width=100)
        self.status_display.pack(padx=5, pady=5)
        
        # Test buttons
        test_group = ttk.LabelFrame(test_frame, text="Testing")
        test_group.pack(fill='x', padx=10, pady=5)
        
        self.test_all_btn = ttk.Button(test_group, text="Run All Tests", command=self.run_all_tests)
        self.test_all_btn.pack(side='left', padx=5, pady=5)
        
        self.test_lab1_btn = ttk.Button(test_group, text="Test Lab 1", command=self.test_lab1)
        self.test_lab1_btn.pack(side='left', padx=5, pady=5)
        
        self.test_lab3_btn = ttk.Button(test_group, text="Test Lab 3", command=self.test_lab3)
        self.test_lab3_btn.pack(side='left', padx=5, pady=5)
        
        self.test_lab4_btn = ttk.Button(test_group, text="Test Lab 4", command=self.test_lab4)
        self.test_lab4_btn.pack(side='left', padx=5, pady=5)
        
        # Test results
        ttk.Label(test_frame, text="Test Results:").pack(anchor='w', padx=10, pady=(10,0))
        
        results_frame = tk.Frame(test_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.test_results = tk.Text(results_frame, height=15, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.test_results.yview)
        self.test_results.configure(yscrollcommand=scrollbar.set)
        
        self.test_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def update_module_status(self):
        """Update module availability status"""
        status_text = "Module Status:\n"
        status_text += f"Lab 1 (Web Scraping): {'Available' if SCRAPER_AVAILABLE else 'Not Available'}\n"
        status_text += f"Lab 3 (Data Processing): {'Available' if LAB3_AVAILABLE else 'Not Available'}\n"
        status_text += f"Lab 4 (Time Series): {'Available' if LAB4_AVAILABLE else 'Not Available'}\n"
        status_text += f"Lab 6 (Advanced Analysis): {'Available' if LAB6_AVAILABLE else 'Not Available'}\n"
        
        self.status_display.delete(1.0, tk.END)
        self.status_display.insert(1.0, status_text)

    # ... (остальные методы остаются без изменений)
    # start_web_scraping, select_dataset_folder, create_annotation, split_to_xy, 
    # split_by_years, split_by_weeks, search_date, load_timeseries_data, 
    # analyze_stationarity, build_arima_model, generate_forecast, 
    # run_all_tests, test_lab1, test_lab3, test_lab4, log

    def start_web_scraping(self):
        """Start web scraping for currency data from Central Bank of Russia"""
        if not SCRAPER_AVAILABLE:
            messagebox.showwarning("Warning", "Lab 1 module not available")
            return
            
        try:
            # Get year from input field
            year_text = self.start_year_entry.get().strip()
            if not year_text:
                messagebox.showwarning("Warning", "Please enter a start year")
                return
                
            try:
                start_year = int(year_text)
                if start_year < 1990 or start_year > datetime.datetime.now().year:
                    messagebox.showwarning("Warning", "Please enter a valid year (1990-current)")
                    return
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid year number")
                return
            
            self.scraping_results.insert(tk.END, f"Starting currency data scraping from year {start_year}...\n")
            self.scraping_results.see(tk.END)
            
            scraper = CurrencyScraper()
            
            # Correct method call with start year
            data = scraper.scrape_data(start_year=start_year)
            
            if data and len(data) > 0:
                # Convert data to DataFrame for compatibility
                df = pd.DataFrame(data, columns=['date', 'rate'])
                self.scraping_results.insert(tk.END, f"Scraping completed! Found {len(df)} records\n")
                self.current_data = df
                
                # Save scraped data
                filename = filedialog.asksaveasfilename(
                    title="Save Scraped Data", 
                    defaultextension=".csv",
                    filetypes=[("CSV Files", "*.csv")]
                )
                if filename:
                    df.to_csv(filename, index=False)
                    self.scraping_results.insert(tk.END, f"Data saved to: {filename}\n")
                    
                # Show first few records
                self.scraping_results.insert(tk.END, "\nFirst 5 records:\n")
                for i, (date, rate) in enumerate(data[:5]):
                    self.scraping_results.insert(tk.END, f"  {date}: {rate}\n")
            else:
                self.scraping_results.insert(tk.END, "No data found or scraping failed\n")
                
        except Exception as e:
            error_msg = f"Scraping error: {str(e)}\n"
            self.scraping_results.insert(tk.END, error_msg)
            messagebox.showerror("Error", error_msg)
        
        self.scraping_results.see(tk.END)

    def select_dataset_folder(self):
        """Select folder containing dataset"""
        folderpath = filedialog.askdirectory(title='Select Dataset Folder')
        if folderpath:
            self.dataset_path = folderpath
            self.dataset_path_label.config(text=folderpath)
            self.lab3_log.insert(tk.END, f"Selected dataset folder: {folderpath}\n")
            self.lab3_log.see(tk.END)

    def create_annotation(self):
        """Create annotation file for current dataset"""
        if not self.dataset_path:
            messagebox.showwarning("Warning", "Please select a dataset folder first")
            return
            
        filepath = filedialog.asksaveasfilename(
            title='Save Annotation File', 
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        
        if filepath:
            try:
                success = create_annotation_file(self.dataset_path, filepath)
                if success:
                    self.lab3_log.insert(tk.END, f"Annotation file created: {filepath}\n")
                else:
                    self.lab3_log.insert(tk.END, f"Failed to create annotation file\n")
            except Exception as e:
                self.lab3_log.insert(tk.END, f"Error creating annotation: {str(e)}\n")
            
            self.lab3_log.see(tk.END)

    def split_to_xy(self):
        """Split dataset to X and Y files"""
        if not self.dataset_path:
            messagebox.showwarning("Warning", "Please select a dataset folder first")
            return
            
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        if not os.path.exists(dataset_file):
            messagebox.showwarning("Warning", "dataset.csv not found")
            return
            
        try:
            processor = CurrencyDataProcessor(dataset_file)
            success = processor.split_to_x_y()
            if success:
                self.lab3_log.insert(tk.END, "Successfully split data into X.csv and Y.csv\n")
            else:
                self.lab3_log.insert(tk.END, "Failed to split data\n")
        except Exception as e:
            self.lab3_log.insert(tk.END, f"Error: {str(e)}\n")
        
        self.lab3_log.see(tk.END)

    def split_by_years(self):
        """Split dataset by years"""
        if not self.dataset_path:
            messagebox.showwarning("Warning", "Please select a dataset folder first")
            return
            
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        if not os.path.exists(dataset_file):
            messagebox.showwarning("Warning", "dataset.csv not found")
            return
            
        try:
            processor = CurrencyDataProcessor(dataset_file)
            output_dir = os.path.join(self.dataset_path, "yearly_data")
            files = processor.split_by_years(output_dir)
            self.lab3_log.insert(tk.END, f"Created {len(files)} yearly files in {output_dir}\n")
        except Exception as e:
            self.lab3_log.insert(tk.END, f"Error: {str(e)}\n")
        
        self.lab3_log.see(tk.END)

    def split_by_weeks(self):
        """Split dataset by weeks"""
        if not self.dataset_path:
            messagebox.showwarning("Warning", "Please select a dataset folder first")
            return
            
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        if not os.path.exists(dataset_file):
            messagebox.showwarning("Warning", "dataset.csv not found")
            return
            
        try:
            processor = CurrencyDataProcessor(dataset_file)
            output_dir = os.path.join(self.dataset_path, "weekly_data")
            files = processor.split_by_weeks(output_dir)
            self.lab3_log.insert(tk.END, f"Created {len(files)} weekly files in {output_dir}\n")
        except Exception as e:
            self.lab3_log.insert(tk.END, f"Error: {str(e)}\n")
        
        self.lab3_log.see(tk.END)

    def search_date(self):
        """Search for data on specific date"""
        if not self.dataset_path:
            messagebox.showwarning("Warning", "Please select a dataset folder first")
            return
            
        date_text = self.date_input.get().strip()
        if not date_text or date_text == "YYYY-MM-DD":
            messagebox.showwarning("Warning", "Please enter a date")
            return
            
        try:
            search_date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD")
            return
            
        search_method = self.search_method_combo.get()
        rate = None
        
        try:
            dataset_file = os.path.join(self.dataset_path, "dataset.csv")
            
            if search_method == "Single File":
                rate = get_rate_single_file(search_date, dataset_file)
            elif search_method == "X/Y Files":
                x_file = os.path.join(self.dataset_path, "X.csv")
                y_file = os.path.join(self.dataset_path, "Y.csv")
                rate = get_rate_x_y(search_date, x_file, y_file)
            elif search_method == "Yearly Files":
                yearly_dir = os.path.join(self.dataset_path, "yearly_data")
                rate = get_rate_year_files(search_date, yearly_dir)
            elif search_method == "Weekly Files":
                weekly_dir = os.path.join(self.dataset_path, "weekly_data")
                rate = get_rate_week_files(search_date, weekly_dir)
                
            if rate is not None:
                self.search_result.delete(1.0, tk.END)
                self.search_result.insert(1.0, f"Rate for {date_text}: {rate}")
                self.lab3_log.insert(tk.END, f"Found rate for {date_text}: {rate}\n")
            else:
                self.search_result.delete(1.0, tk.END)
                self.search_result.insert(1.0, f"No data found for {date_text}")
                self.lab3_log.insert(tk.END, f"No data found for {date_text}\n")
                
        except Exception as e:
            error_text = f"Search error: {str(e)}"
            self.search_result.delete(1.0, tk.END)
            self.search_result.insert(1.0, error_text)
            self.lab3_log.insert(tk.END, error_text + "\n")
        
        self.lab3_log.see(tk.END)

    def load_timeseries_data(self):
        """Load time series data for analysis"""
        filename = filedialog.askopenfilename(
            title="Open Time Series Data", 
            filetypes=[("CSV Files", "*.csv")]
        )
        
        if filename:
            try:
                self.ts_analyzer = TimeSeriesAnalyzer()
                self.timeseries_data = self.ts_analyzer.load_data(filename)
                
                info_text = f"Loaded time series data: {filename}\n"
                info_text += f"Data shape: {self.timeseries_data.shape}\n"
                info_text += f"Date range: {self.timeseries_data['date'].min()} to {self.timeseries_data['date'].max()}\n"
                
                self.data_info_label.config(text=f"Data loaded: {os.path.basename(filename)}")
                self.lab4_results.insert(tk.END, info_text)
                self.lab4_results.see(tk.END)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def analyze_stationarity(self):
        """Perform stationarity analysis"""
        if not hasattr(self, 'timeseries_data'):
            messagebox.showwarning("Warning", "Please load time series data first")
            return
            
        try:
            result = self.ts_analyzer.test_stationarity(self.timeseries_data)
            
            result_text = "=== Stationarity Analysis ===\n"
            for key, value in result.items():
                result_text += f"{key}: {value}\n"
            
            self.lab4_results.insert(tk.END, result_text)
            self.lab4_results.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Stationarity analysis failed: {str(e)}")

    def build_arima_model(self):
        """Build ARIMA model"""
        if not hasattr(self, 'timeseries_data'):
            messagebox.showwarning("Warning", "Please load time series data first")
            return
            
        try:
            self.ts_analyzer.fit_arima(self.timeseries_data)
            self.lab4_results.insert(tk.END, "ARIMA model built successfully\n")
            self.lab4_results.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"ARIMA model building failed: {str(e)}")

    def generate_forecast(self):
        """Generate forecast using ARIMA model"""
        if not hasattr(self, 'ts_analyzer') or not hasattr(self.ts_analyzer, 'model_fitted'):
            messagebox.showwarning("Warning", "Please build ARIMA model first")
            return
            
        try:
            forecast = self.ts_analyzer.forecast_arima(steps=30)
            
            forecast_text = "=== 30-Day Forecast ===\n"
            forecast_text += f"Forecast values: {forecast}\n"
            
            self.lab4_results.insert(tk.END, forecast_text)
            self.lab4_results.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Forecast generation failed: {str(e)}")

    def run_all_tests(self):
        """Run all module tests"""
        self.test_results.delete(1.0, tk.END)
        self.test_results.insert(tk.END, "=== Running All Tests ===\n")
        
        self.test_lab1()
        self.test_lab3()
        self.test_lab4()
        
        self.test_results.insert(tk.END, "\n=== All Tests Completed ===")
        self.test_results.see(tk.END)

    def test_lab1(self):
        """Test Lab 1 functionality"""
        self.test_results.insert(tk.END, "\n--- Testing Lab 1: Web Scraping ---\n")
        if SCRAPER_AVAILABLE:
            self.test_results.insert(tk.END, "✓ Lab 1 module imported successfully\n")
            # Add more specific tests here
        else:
            self.test_results.insert(tk.END, "✗ Lab 1 module not available\n")

    def test_lab3(self):
        """Test Lab 3 functionality"""
        self.test_results.insert(tk.END, "\n--- Testing Lab 3: Data Processing ---\n")
        if LAB3_AVAILABLE:
            self.test_results.insert(tk.END, "✓ Lab 3 modules imported successfully\n")
            # Add more specific tests here
        else:
            self.test_results.insert(tk.END, "✗ Lab 3 modules not available\n")

    def test_lab4(self):
        """Test Lab 4 functionality"""
        self.test_results.insert(tk.END, "\n--- Testing Lab 4: Time Series ---\n")
        if LAB4_AVAILABLE:
            self.test_results.insert(tk.END, "✓ Lab 4 module imported successfully\n")
            # Add more specific tests here
        else:
            self.test_results.insert(tk.END, "✗ Lab 4 module not available\n")
    
    def setup_lab6_tab(self):
        """Setup Lab 6: Advanced Time Series Analysis with full functionality"""
        if not LAB6_AVAILABLE:
            lab6_frame = ttk.Frame(self.notebook)
            self.notebook.add(lab6_frame, text="Lab 6: Advanced Analysis")
            ttk.Label(lab6_frame, text="Lab 6 modules not available").pack(pady=20)
            return
    
        lab6_frame = ttk.Frame(self.notebook)
        self.notebook.add(lab6_frame, text="Lab 6: Advanced Analysis")
    
        # Create notebook for Lab 6 sections
        lab6_notebook = ttk.Notebook(lab6_frame)
        lab6_notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
        # Tab 1: Data Analysis
        analysis_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(analysis_tab, text="1. Data Analysis")
        self.setup_lab6_analysis_tab(analysis_tab)
    
        # Tab 2: Model Training
        training_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(training_tab, text="2. Model Training")
        self.setup_lab6_training_tab(training_tab)
    
        # Tab 3: Hyperparameter Tuning
        tuning_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(tuning_tab, text="3. Hyperparameter Tuning")
        self.setup_lab6_tuning_tab(tuning_tab)
    
        # Tab 4: Model Evaluation
        eval_tab = ttk.Frame(lab6_notebook)
        lab6_notebook.add(eval_tab, text="4. Model Evaluation")
        self.setup_lab6_evaluation_tab(eval_tab)

    def setup_lab6_analysis_tab(self, parent):
        """Setup Lab 6 Data Analysis tab"""
        # Data loading section
        load_frame = ttk.LabelFrame(parent, text="Data Loading")
        load_frame.pack(fill='x', padx=10, pady=5)
    
        ttk.Button(load_frame, text="Load Dataset for Analysis", 
              command=self.load_lab6_data).pack(padx=5, pady=5)
    
        self.lab6_data_info = ttk.Label(load_frame, text="No data loaded")
        self.lab6_data_info.pack(padx=5, pady=5)
    
        # Analysis controls
        analysis_frame = ttk.LabelFrame(parent, text="Advanced Analysis")
        analysis_frame.pack(fill='x', padx=10, pady=5)
    
        analysis_buttons = ttk.Frame(analysis_frame)
        analysis_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(analysis_buttons, text="Comprehensive Analysis",
              command=self.run_lab6_analysis).pack(side='left', padx=5, pady=5)
        ttk.Button(analysis_buttons, text="Stationarity Tests",
              command=self.run_stationarity_tests).pack(side='left', padx=5, pady=5)
        ttk.Button(analysis_buttons, text="Autocorrelation Analysis",
              command=self.run_autocorrelation_analysis).pack(side='left', padx=5, pady=5)
        ttk.Button(analysis_buttons, text="Seasonal Decomposition",
              command=self.run_seasonal_decomposition).pack(side='left', padx=5, pady=5)
    
        # Results display
        results_frame = ttk.LabelFrame(parent, text="Analysis Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_analysis_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_analysis_results.yview)
        self.lab6_analysis_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_analysis_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_lab6_training_tab(self, parent):
        """Setup Lab 6 Model Training tab"""
        # Data preparation
        prep_frame = ttk.LabelFrame(parent, text="Data Preparation")
        prep_frame.pack(fill='x', padx=10, pady=5)
    
        ttk.Button(prep_frame, text="Prepare Data for Modeling",
              command=self.prepare_lab6_data).pack(padx=5, pady=5)
    
        self.lab6_prep_info = ttk.Label(prep_frame, text="Data not prepared")
        self.lab6_prep_info.pack(padx=5, pady=5)
    
        # Model selection
        model_frame = ttk.LabelFrame(parent, text="Model Selection")
        model_frame.pack(fill='x', padx=10, pady=5)
    
        model_buttons = ttk.Frame(model_frame)
        model_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(model_buttons, text="Train SARIMA Model",
              command=self.train_sarima_model).pack(side='left', padx=5, pady=5)
        ttk.Button(model_buttons, text="Train Linear Regression",
              command=self.train_linear_model).pack(side='left', padx=5, pady=5)
        ttk.Button(model_buttons, text="Train Random Forest",
              command=self.train_random_forest).pack(side='left', padx=5, pady=5)
        ttk.Button(model_buttons, text="Evaluate All Models",
              command=self.evaluate_lab6_models).pack(side='left', padx=5, pady=5)
    
        # Training results
        results_frame = ttk.LabelFrame(parent, text="Training Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_training_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_training_results.yview)
        self.lab6_training_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_training_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_lab6_tuning_tab(self, parent):
        """Setup Lab 6 Hyperparameter Tuning tab"""
        # Tuning controls
        tuning_frame = ttk.LabelFrame(parent, text="Hyperparameter Tuning")
        tuning_frame.pack(fill='x', padx=10, pady=5)
    
        tuning_buttons = ttk.Frame(tuning_frame)
        tuning_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(tuning_buttons, text="Tune SARIMA Parameters",
              command=self.tune_sarima_params).pack(side='left', padx=5, pady=5)
        ttk.Button(tuning_buttons, text="Tune Random Forest Parameters",
              command=self.tune_rf_params).pack(side='left', padx=5, pady=5)
        ttk.Button(tuning_buttons, text="Save Tuning Results",
              command=self.save_tuning_results).pack(side='left', padx=5, pady=5)
    
        # Parameter configuration
        param_frame = ttk.LabelFrame(parent, text="Parameter Configuration")
        param_frame.pack(fill='x', padx=10, pady=5)
    
        # SARIMA parameters
        sarima_frame = ttk.Frame(param_frame)
        sarima_frame.pack(fill='x', padx=5, pady=5)
    
        ttk.Label(sarima_frame, text="SARIMA Order (p,d,q):").grid(row=0, column=0, sticky='w', padx=5)
        self.sarima_order = ttk.Entry(sarima_frame, width=15)
        self.sarima_order.grid(row=0, column=1, padx=5)
        self.sarima_order.insert(0, "1,1,1")
    
        ttk.Label(sarima_frame, text="Seasonal Order (P,D,Q,s):").grid(row=0, column=2, sticky='w', padx=5)
        self.seasonal_order = ttk.Entry(sarima_frame, width=15)
        self.seasonal_order.grid(row=0, column=3, padx=5)
        self.seasonal_order.insert(0, "1,1,1,7")
    
        # Random Forest parameters
        rf_frame = ttk.Frame(param_frame)
        rf_frame.pack(fill='x', padx=5, pady=5)
    
        ttk.Label(rf_frame, text="n_estimators:").grid(row=0, column=0, sticky='w', padx=5)
        self.n_estimators = ttk.Entry(rf_frame, width=10)
        self.n_estimators.grid(row=0, column=1, padx=5)
        self.n_estimators.insert(0, "100")
    
        ttk.Label(rf_frame, text="max_depth:").grid(row=0, column=2, sticky='w', padx=5)
        self.max_depth = ttk.Entry(rf_frame, width=10)
        self.max_depth.grid(row=0, column=3, padx=5)
        self.max_depth.insert(0, "10")
    
        # Tuning results
        results_frame = ttk.LabelFrame(parent, text="Tuning Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_tuning_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_tuning_results.yview)
        self.lab6_tuning_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_tuning_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def setup_lab6_evaluation_tab(self, parent):
        """Setup Lab 6 Model Evaluation tab"""
        # Model deployment
        deploy_frame = ttk.LabelFrame(parent, text="Model Deployment")
        deploy_frame.pack(fill='x', padx=10, pady=5)
    
        deploy_buttons = ttk.Frame(deploy_frame)
        deploy_buttons.pack(fill='x', padx=5, pady=5)
    
        ttk.Button(deploy_buttons, text="Save Best Model",
              command=self.save_best_model).pack(side='left', padx=5, pady=5)
        ttk.Button(deploy_buttons, text="Load Saved Model",
              command=self.load_saved_model).pack(side='left', padx=5, pady=5)
        ttk.Button(deploy_buttons, text="Generate Report",
              command=self.generate_lab6_report).pack(side='left', padx=5, pady=5)
    
        # Prediction interface
        predict_frame = ttk.LabelFrame(parent, text="Model Prediction")
        predict_frame.pack(fill='x', padx=10, pady=5)
    
        predict_controls = ttk.Frame(predict_frame)
        predict_controls.pack(fill='x', padx=5, pady=5)
    
        ttk.Label(predict_controls, text="Forecast Steps:").pack(side='left', padx=5)
        self.forecast_steps_entry = ttk.Entry(predict_controls, width=10)
        self.forecast_steps_entry.pack(side='left', padx=5)
        self.forecast_steps_entry.insert(0, "30")
    
        ttk.Button(predict_controls, text="Make Prediction",
              command=self.make_lab6_prediction).pack(side='left', padx=5)
    
        ttk.Label(predict_controls, text="Model:").pack(side='left', padx=5)
        self.model_selector = ttk.Combobox(predict_controls, 
                                     values=["SARIMA", "Linear Regression", "Random Forest"])
        self.model_selector.set("SARIMA")
        self.model_selector.pack(side='left', padx=5)
    
        # Evaluation results
        results_frame = ttk.LabelFrame(parent, text="Evaluation Results")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        self.lab6_evaluation_results = tk.Text(results_frame, height=20, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab6_evaluation_results.yview)
        self.lab6_evaluation_results.configure(yscrollcommand=scrollbar.set)
    
        self.lab6_evaluation_results.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def log(self, message: str):
        """Add message to main log"""
        print(f"[LOG] {message}")


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = IntegratedAnalyticsPlatform(root)
    root.mainloop()


if __name__ == "__main__":
    main()