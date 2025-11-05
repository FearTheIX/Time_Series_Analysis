"""
Main integrated GUI application combining all laboratory works
Lab 1: Web Scraping, Lab 2: Data Processing, Lab 3: GUI, Lab 4: Time Series Analysis
"""

import sys
import os
import datetime
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTextEdit, QFileDialog, QComboBox, QMessageBox,
                               QGroupBox, QFormLayout, QTabWidget)
from PySide6.QtCore import Qt

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


class IntegratedAnalyticsPlatform(QMainWindow):
    """
    Main integrated GUI window combining all laboratory works
    """
    
    def __init__(self):
        """Initialize the main window with all laboratory features"""
        super().__init__()
        self.dataset_path = ""
        self.current_data = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface with tabs for each lab"""
        self.setWindowTitle("Integrated Analytics Platform - All Labs")
        self.setGeometry(100, 100, 1000, 800)
        
        # Central widget with tab layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs for each laboratory
        if SCRAPER_AVAILABLE:
            self.setup_lab1_tab()
        
        if LAB3_AVAILABLE:
            self.setup_lab3_tab()
            
        if LAB4_AVAILABLE:
            self.setup_lab4_tab()
        
        # Add testing tab
        self.setup_testing_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        self.log("Application started successfully")
        self.update_module_status()
    
    def setup_lab1_tab(self):
        """Setup Lab 1: Web Scraping tab"""
        lab1_tab = QWidget()
        layout = QVBoxLayout(lab1_tab)
        
        # Web scraping section
        scraping_group = QGroupBox("Web Scraping (Lab 1)")
        scraping_layout = QFormLayout(scraping_group)
        
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("https://www.example.com/currency-rates")
        
        self.scrape_btn = QPushButton("Start Scraping")
        self.scrape_btn.clicked.connect(self.start_web_scraping)
        
        scraping_layout.addRow("Target URL:", self.url_entry)
        scraping_layout.addRow(self.scrape_btn)
        
        # Results display
        self.scraping_results = QTextEdit()
        self.scraping_results.setReadOnly(True)
        
        layout.addWidget(scraping_group)
        layout.addWidget(QLabel("Scraping Results:"))
        layout.addWidget(self.scraping_results)
        
        self.tab_widget.addTab(lab1_tab, "Lab 1: Web Scraping")
    
    def setup_lab3_tab(self):
        """Setup Lab 3: Data Processing tab"""
        lab3_tab = QWidget()
        layout = QVBoxLayout(lab3_tab)
        
        # Dataset selection
        dataset_group = QGroupBox("Dataset Selection")
        dataset_layout = QFormLayout(dataset_group)
        
        self.dataset_path_label = QLabel("No dataset selected")
        self.select_dataset_btn = QPushButton("Select Dataset Folder")
        self.select_dataset_btn.clicked.connect(self.select_dataset_folder)
        
        dataset_layout.addRow("Dataset:", self.dataset_path_label)
        dataset_layout.addRow(self.select_dataset_btn)
        
        # Data processing buttons
        processing_group = QGroupBox("Data Processing")
        processing_layout = QVBoxLayout(processing_group)
        
        self.create_annotation_btn = QPushButton("Create Annotation File")
        self.create_annotation_btn.clicked.connect(self.create_annotation)
        
        self.split_xy_btn = QPushButton("Split to X and Y Files")
        self.split_xy_btn.clicked.connect(self.split_to_xy)
        
        self.split_yearly_btn = QPushButton("Split by Years")
        self.split_yearly_btn.clicked.connect(self.split_by_years)
        
        self.split_weekly_btn = QPushButton("Split by Weeks")
        self.split_weekly_btn.clicked.connect(self.split_by_weeks)
        
        processing_layout.addWidget(self.create_annotation_btn)
        processing_layout.addWidget(self.split_xy_btn)
        processing_layout.addWidget(self.split_yearly_btn)
        processing_layout.addWidget(self.split_weekly_btn)
        
        # Date search section
        search_group = QGroupBox("Date Search")
        search_layout = QFormLayout(search_group)
        
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        
        self.search_method_combo = QComboBox()
        self.search_method_combo.addItems([
            "Single File", 
            "X/Y Files", 
            "Yearly Files", 
            "Weekly Files"
        ])
        
        self.search_btn = QPushButton("Search Date")
        self.search_btn.clicked.connect(self.search_date)
        
        self.search_result = QTextEdit()
        self.search_result.setReadOnly(True)
        self.search_result.setMaximumHeight(80)
        
        search_layout.addRow("Date:", self.date_input)
        search_layout.addRow("Method:", self.search_method_combo)
        search_layout.addRow(self.search_btn)
        search_layout.addRow("Result:", self.search_result)
        
        # Log display
        self.lab3_log = QTextEdit()
        self.lab3_log.setReadOnly(True)
        
        layout.addWidget(dataset_group)
        layout.addWidget(processing_group)
        layout.addWidget(search_group)
        layout.addWidget(QLabel("Processing Log:"))
        layout.addWidget(self.lab3_log)
        
        self.tab_widget.addTab(lab3_tab, "Lab 3: Data Processing")
    
    def setup_lab4_tab(self):
        """Setup Lab 4: Time Series Analysis tab"""
        lab4_tab = QWidget()
        layout = QVBoxLayout(lab4_tab)
        
        # Data loading section
        load_group = QGroupBox("Data Loading")
        load_layout = QHBoxLayout(load_group)
        
        self.load_data_btn = QPushButton("Load Time Series Data")
        self.load_data_btn.clicked.connect(self.load_timeseries_data)
        
        self.data_info_label = QLabel("No data loaded")
        
        load_layout.addWidget(self.load_data_btn)
        load_layout.addWidget(self.data_info_label)
        
        # Analysis controls
        analysis_group = QGroupBox("Time Series Analysis")
        analysis_layout = QHBoxLayout(analysis_group)
        
        self.stationarity_btn = QPushButton("Stationarity Analysis")
        self.stationarity_btn.clicked.connect(self.analyze_stationarity)
        
        self.build_arima_btn = QPushButton("Build ARIMA Model")
        self.build_arima_btn.clicked.connect(self.build_arima_model)
        
        self.forecast_btn = QPushButton("Generate Forecast")
        self.forecast_btn.clicked.connect(self.generate_forecast)
        
        analysis_layout.addWidget(self.stationarity_btn)
        analysis_layout.addWidget(self.build_arima_btn)
        analysis_layout.addWidget(self.forecast_btn)
        
        # Results display
        self.lab4_results = QTextEdit()
        self.lab4_results.setReadOnly(True)
        
        layout.addWidget(load_group)
        layout.addWidget(analysis_group)
        layout.addWidget(QLabel("Analysis Results:"))
        layout.addWidget(self.lab4_results)
        
        self.tab_widget.addTab(lab4_tab, "Lab 4: Time Series")
    
    def setup_testing_tab(self):
        """Setup testing and diagnostics tab"""
        test_tab = QWidget()
        layout = QVBoxLayout(test_tab)
        
        # Module status
        status_group = QGroupBox("Module Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setMaximumHeight(150)
        
        status_layout.addWidget(self.status_display)
        
        # Test buttons
        test_group = QGroupBox("Testing")
        test_layout = QHBoxLayout(test_group)
        
        self.test_all_btn = QPushButton("Run All Tests")
        self.test_all_btn.clicked.connect(self.run_all_tests)
        
        self.test_lab1_btn = QPushButton("Test Lab 1")
        self.test_lab1_btn.clicked.connect(self.test_lab1)
        
        self.test_lab3_btn = QPushButton("Test Lab 3")
        self.test_lab3_btn.clicked.connect(self.test_lab3)
        
        self.test_lab4_btn = QPushButton("Test Lab 4")
        self.test_lab4_btn.clicked.connect(self.test_lab4)
        
        test_layout.addWidget(self.test_all_btn)
        test_layout.addWidget(self.test_lab1_btn)
        test_layout.addWidget(self.test_lab3_btn)
        test_layout.addWidget(self.test_lab4_btn)
        
        # Test results
        self.test_results = QTextEdit()
        self.test_results.setReadOnly(True)
        
        layout.addWidget(status_group)
        layout.addWidget(test_group)
        layout.addWidget(QLabel("Test Results:"))
        layout.addWidget(self.test_results)
        
        self.tab_widget.addTab(test_tab, "Testing & Diagnostics")
    
    def update_module_status(self):
        """Update module availability status"""
        status_text = "Module Status:\n"
        status_text += f"Lab 1 (Web Scraping): {'Available' if SCRAPER_AVAILABLE else 'Not Available'}\n"
        status_text += f"Lab 3 (Data Processing): {'Available' if LAB3_AVAILABLE else 'Not Available'}\n"
        status_text += f"Lab 4 (Time Series): {'Available' if LAB4_AVAILABLE else 'Not Available'}\n"
        
        self.status_display.setText(status_text)
    
    # Lab 1 Methods
    def start_web_scraping(self):
        """Start web scraping for currency data"""
        if not SCRAPER_AVAILABLE:
            QMessageBox.warning(self, "Warning", "Lab 1 module not available")
            return
            
        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL")
            return
            
        try:
            self.scraping_results.append(f"Starting scraping from: {url}")
            
            scraper = CurrencyScraper()
            # Note: Adjust method name based on actual implementation
            data = scraper.scrape_currency_data(url)
            
            if data is not None and not data.empty:
                self.scraping_results.append(f"Scraping completed! Found {len(data)} records")
                self.current_data = data
                
                # Save scraped data
                filename, _ = QFileDialog.getSaveFileName(
                    self, "Save Scraped Data", "", "CSV Files (*.csv)"
                )
                if filename:
                    data.to_csv(filename, index=False)
                    self.scraping_results.append(f"Data saved to: {filename}")
            else:
                self.scraping_results.append("No data found or scraping failed")
                
        except Exception as e:
            error_msg = f"Scraping error: {str(e)}"
            self.scraping_results.append(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
    
    # Lab 3 Methods
    def select_dataset_folder(self):
        """Select folder containing dataset"""
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Dataset Folder')
        if folderpath:
            self.dataset_path = folderpath
            self.dataset_path_label.setText(folderpath)
            self.lab3_log.append(f"Selected dataset folder: {folderpath}")
    
    def create_annotation(self):
        """Create annotation file for current dataset"""
        if not self.dataset_path:
            QMessageBox.warning(self, "Warning", "Please select a dataset folder first")
            return
            
        filepath, _ = QFileDialog.getSaveFileName(
            self, 'Save Annotation File', '', 'CSV Files (*.csv)'
        )
        
        if filepath:
            success = create_annotation_file(self.dataset_path, filepath)
            if success:
                self.lab3_log.append(f"Annotation file created: {filepath}")
            else:
                self.lab3_log.append(f"Failed to create annotation file")
    
    def split_to_xy(self):
        """Split dataset to X and Y files"""
        if not self.dataset_path:
            QMessageBox.warning(self, "Warning", "Please select a dataset folder first")
            return
            
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        if not os.path.exists(dataset_file):
            QMessageBox.warning(self, "Warning", "dataset.csv not found")
            return
            
        try:
            processor = CurrencyDataProcessor(dataset_file)
            success = processor.split_to_x_y()
            if success:
                self.lab3_log.append("Successfully split data into X.csv and Y.csv")
            else:
                self.lab3_log.append("Failed to split data")
        except Exception as e:
            self.lab3_log.append(f"Error: {str(e)}")
    
    def split_by_years(self):
        """Split dataset by years"""
        if not self.dataset_path:
            QMessageBox.warning(self, "Warning", "Please select a dataset folder first")
            return
            
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        if not os.path.exists(dataset_file):
            QMessageBox.warning(self, "Warning", "dataset.csv not found")
            return
            
        try:
            processor = CurrencyDataProcessor(dataset_file)
            output_dir = os.path.join(self.dataset_path, "yearly_data")
            files = processor.split_by_years(output_dir)
            self.lab3_log.append(f"Created {len(files)} yearly files in {output_dir}")
        except Exception as e:
            self.lab3_log.append(f"Error: {str(e)}")
    
    def split_by_weeks(self):
        """Split dataset by weeks"""
        if not self.dataset_path:
            QMessageBox.warning(self, "Warning", "Please select a dataset folder first")
            return
            
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        if not os.path.exists(dataset_file):
            QMessageBox.warning(self, "Warning", "dataset.csv not found")
            return
            
        try:
            processor = CurrencyDataProcessor(dataset_file)
            output_dir = os.path.join(self.dataset_path, "weekly_data")
            files = processor.split_by_weeks(output_dir)
            self.lab3_log.append(f"Created {len(files)} weekly files in {output_dir}")
        except Exception as e:
            self.lab3_log.append(f"Error: {str(e)}")
    
    def search_date(self):
        """Search for data on specific date"""
        if not self.dataset_path:
            QMessageBox.warning(self, "Warning", "Please select a dataset folder first")
            return
            
        date_text = self.date_input.text().strip()
        if not date_text:
            QMessageBox.warning(self, "Warning", "Please enter a date")
            return
            
        try:
            search_date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid date format. Use YYYY-MM-DD")
            return
            
        search_method = self.search_method_combo.currentText()
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
                self.search_result.setText(f"Rate for {date_text}: {rate}")
                self.lab3_log.append(f"Found rate for {date_text}: {rate}")
            else:
                self.search_result.setText(f"No data found for {date_text}")
                self.lab3_log.append(f"No data found for {date_text}")
                
        except Exception as e:
            error_text = f"Search error: {str(e)}"
            self.search_result.setText(error_text)
            self.lab3_log.append(error_text)
    
    # Lab 4 Methods
    def load_timeseries_data(self):
        """Load time series data for analysis"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Time Series Data", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                self.ts_analyzer = TimeSeriesAnalyzer()
                self.timeseries_data = self.ts_analyzer.load_data(filename)
                
                info_text = f"Loaded time series data: {filename}\n"
                info_text += f"Data shape: {self.timeseries_data.shape}\n"
                info_text += f"Date range: {self.timeseries_data['date'].min()} to {self.timeseries_data['date'].max()}\n"
                
                self.data_info_label.setText(f"Data loaded: {os.path.basename(filename)}")
                self.lab4_results.append(info_text)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
    
    def analyze_stationarity(self):
        """Perform stationarity analysis"""
        if not hasattr(self, 'timeseries_data'):
            QMessageBox.warning(self, "Warning", "Please load time series data first")
            return
            
        try:
            result = self.ts_analyzer.test_stationarity(self.timeseries_data)
            
            result_text = "=== Stationarity Analysis ===\n"
            for key, value in result.items():
                result_text += f"{key}: {value}\n"
            
            self.lab4_results.append(result_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Stationarity analysis failed: {str(e)}")
    
    def build_arima_model(self):
        """Build ARIMA model"""
        if not hasattr(self, 'timeseries_data'):
            QMessageBox.warning(self, "Warning", "Please load time series data first")
            return
            
        try:
            self.ts_analyzer.fit_arima(self.timeseries_data)
            self.lab4_results.append("ARIMA model built successfully\n")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"ARIMA model building failed: {str(e)}")
    
    def generate_forecast(self):
        """Generate forecast using ARIMA model"""
        if not hasattr(self, 'ts_analyzer') or not hasattr(self.ts_analyzer, 'model_fitted'):
            QMessageBox.warning(self, "Warning", "Please build ARIMA model first")
            return
            
        try:
            forecast = self.ts_analyzer.forecast_arima(steps=30)
            
            forecast_text = "=== 30-Day Forecast ===\n"
            forecast_text += f"Forecast values: {forecast}\n"
            
            self.lab4_results.append(forecast_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Forecast generation failed: {str(e)}")
    
    # Testing Methods
    def run_all_tests(self):
        """Run all module tests"""
        self.test_results.clear()
        self.test_results.append("=== Running All Tests ===\n")
        
        self.test_lab1()
        self.test_lab3()
        self.test_lab4()
        
        self.test_results.append("\n=== All Tests Completed ===")
    
    def test_lab1(self):
        """Test Lab 1 functionality"""
        self.test_results.append("\n--- Testing Lab 1: Web Scraping ---")
        if SCRAPER_AVAILABLE:
            self.test_results.append("✓ Lab 1 module imported successfully")
            # Add more specific tests here
        else:
            self.test_results.append("✗ Lab 1 module not available")
    
    def test_lab3(self):
        """Test Lab 3 functionality"""
        self.test_results.append("\n--- Testing Lab 3: Data Processing ---")
        if LAB3_AVAILABLE:
            self.test_results.append("✓ Lab 3 modules imported successfully")
            # Add more specific tests here
        else:
            self.test_results.append("✗ Lab 3 modules not available")
    
    def test_lab4(self):
        """Test Lab 4 functionality"""
        self.test_results.append("\n--- Testing Lab 4: Time Series ---")
        if LAB4_AVAILABLE:
            self.test_results.append("✓ Lab 4 module imported successfully")
            # Add more specific tests here
        else:
            self.test_results.append("✗ Lab 4 module not available")
    
    def log(self, message: str):
        """Add message to main log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        # Could add to a main log display if needed


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    window = IntegratedAnalyticsPlatform()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()