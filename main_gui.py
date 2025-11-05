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

# Import modules from different labs
try:
    from currency_scrapper_v2 import CurrencyScraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False
    print("Warning: Lab 1 module (currency_scrapper_v2) not found")

try:
    from data_processor import CurrencyDataProcessor, get_rate_single_file, get_rate_x_y, get_rate_year_files, get_rate_week_files
    from annotation_creator import create_annotation_file, create_reorganized_dataset
    LAB3_AVAILABLE = True
except ImportError:
    LAB3_AVAILABLE = False
    print("Warning: Lab 3 modules not found")

try:
    from time_series_analyzer import TimeSeriesAnalyzer
    LAB4_AVAILABLE = True
except ImportError:
    LAB4_AVAILABLE = False
    print("Warning: Lab 4 module not found")


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
        scraping_group = ttk.LabelFrame(lab1_frame, text="Web Scraping (Lab 1)")
        scraping_group.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(scraping_group, text="Target URL:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.url_entry = ttk.Entry(scraping_group, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        self.url_entry.insert(0, "https://www.example.com/currency-rates")
        
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
        load_group.pack(fill='x', padx=10, pady=5)
        
        self.load_data_btn = ttk.Button(load_group, text="Load Time Series Data", command=self.load_timeseries_data)
        self.load_data_btn.pack(side='left', padx=5, pady=5)
        
        self.data_info_label = ttk.Label(load_group, text="No data loaded")
        self.data_info_label.pack(side='left', padx=5, pady=5)
        
        # Analysis controls
        analysis_group = ttk.LabelFrame(lab4_frame, text="Time Series Analysis")
        analysis_group.pack(fill='x', padx=10, pady=5)
        
        self.stationarity_btn = ttk.Button(analysis_group, text="Stationarity Analysis", command=self.analyze_stationarity)
        self.stationarity_btn.pack(side='left', padx=5, pady=5)
        
        self.build_arima_btn = ttk.Button(analysis_group, text="Build ARIMA Model", command=self.build_arima_model)
        self.build_arima_btn.pack(side='left', padx=5, pady=5)
        
        self.forecast_btn = ttk.Button(analysis_group, text="Generate Forecast", command=self.generate_forecast)
        self.forecast_btn.pack(side='left', padx=5, pady=5)
        
        # Results display
        ttk.Label(lab4_frame, text="Analysis Results:").pack(anchor='w', padx=10, pady=(10,0))
        
        results_frame = tk.Frame(lab4_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.lab4_results = tk.Text(results_frame, height=15, width=100)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.lab4_results.yview)
        self.lab4_results.configure(yscrollcommand=scrollbar.set)
        
        self.lab4_results.pack(side='left', fill='both', expand=True)
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
        
        self.status_display.delete(1.0, tk.END)
        self.status_display.insert(1.0, status_text)

    def start_web_scraping(self):
        """Start web scraping for currency data"""
        if not SCRAPER_AVAILABLE:
            messagebox.showwarning("Warning", "Lab 1 module not available")
            return
            
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
            
        try:
            self.scraping_results.insert(tk.END, f"Starting scraping from: {url}\n")
            self.scraping_results.see(tk.END)
            
            scraper = CurrencyScraper()
            data = scraper.scrape_currency_data(url)
            
            if data is not None and not data.empty:
                self.scraping_results.insert(tk.END, f"Scraping completed! Found {len(data)} records\n")
                self.current_data = data
                
                # Save scraped data
                filename = filedialog.asksaveasfilename(
                    title="Save Scraped Data", 
                    defaultextension=".csv",
                    filetypes=[("CSV Files", "*.csv")]
                )
                if filename:
                    data.to_csv(filename, index=False)
                    self.scraping_results.insert(tk.END, f"Data saved to: {filename}\n")
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