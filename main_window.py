"""
Main GUI application for Currency Data Processing
"""

import sys
import os
import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QTextEdit, QFileDialog, QComboBox, QMessageBox,
                               QGroupBox, QFormLayout)
from PySide6.QtCore import Qt
from data_processor import (get_rate_single_file, get_rate_x_y, 
                          get_rate_year_files, get_rate_week_files)
from annotation_creator import create_annotation_file, create_reorganized_dataset


class CurrencyDataGUI(QMainWindow):
    """Main GUI window for currency data processing"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        self.dataset_path = ""
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Currency Data Processor")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Dataset selection section
        dataset_group = QGroupBox("Dataset Selection")
        dataset_layout = QFormLayout(dataset_group)
        
        self.dataset_path_label = QLabel("No dataset selected")
        self.select_dataset_btn = QPushButton("Select Dataset Folder")
        self.select_dataset_btn.clicked.connect(self.select_dataset_folder)
        
        dataset_layout.addRow("Dataset:", self.dataset_path_label)
        dataset_layout.addRow(self.select_dataset_btn)
        
        # Annotation creation section
        annotation_group = QGroupBox("Annotation Creation")
        annotation_layout = QVBoxLayout(annotation_group)
        
        self.create_annotation_btn = QPushButton("Create Annotation File")
        self.create_annotation_btn.clicked.connect(self.create_annotation)
        annotation_layout.addWidget(self.create_annotation_btn)
        
        # Dataset reorganization section
        reorganization_group = QGroupBox("Dataset Reorganization")
        reorganization_layout = QFormLayout(reorganization_group)
        
        self.org_type_combo = QComboBox()
        self.org_type_combo.addItems(["yearly", "weekly", "xy"])
        
        self.reorganize_btn = QPushButton("Reorganize Dataset and Create Annotation")
        self.reorganize_btn.clicked.connect(self.reorganize_dataset)
        
        reorganization_layout.addRow("Organization Type:", self.org_type_combo)
        reorganization_layout.addRow(self.reorganize_btn)
        
        # Date search section
        search_group = QGroupBox("Date Search")
        search_layout = QFormLayout(search_group)
        
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        
        self.search_btn = QPushButton("Get Data for Date")
        self.search_btn.clicked.connect(self.search_date)
        
        self.search_method_combo = QComboBox()
        self.search_method_combo.addItems([
            "Single File", 
            "X/Y Files", 
            "Yearly Files", 
            "Weekly Files"
        ])
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMaximumHeight(100)
        
        search_layout.addRow("Date (YYYY-MM-DD):", self.date_input)
        search_layout.addRow("Search Method:", self.search_method_combo)
        search_layout.addRow(self.search_btn)
        search_layout.addRow("Result:", self.result_display)
        
        # Log section
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display)
        
        # Add all groups to main layout
        layout.addWidget(dataset_group)
        layout.addWidget(annotation_group)
        layout.addWidget(reorganization_group)
        layout.addWidget(search_group)
        layout.addWidget(log_group)
        
        self.log("Application started. Please select a dataset folder.")
        
    def select_dataset_folder(self):
        """Select folder containing dataset"""
        folderpath = QFileDialog.getExistingDirectory(self, 'Select Dataset Folder')
        if folderpath:
            self.dataset_path = folderpath
            self.dataset_path_label.setText(folderpath)
            self.log(f"Selected dataset folder: {folderpath}")
            
            # Check if dataset.csv exists in the folder
            dataset_file = os.path.join(folderpath, "dataset.csv")
            if os.path.exists(dataset_file):
                self.log("Found dataset.csv in selected folder")
            else:
                self.log("Warning: dataset.csv not found in selected folder")
    
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
                self.log(f"Annotation file created: {filepath}")
                QMessageBox.information(self, "Success", "Annotation file created successfully")
            else:
                self.log(f"Failed to create annotation file: {filepath}")
                QMessageBox.critical(self, "Error", "Failed to create annotation file")
    
    def reorganize_dataset(self):
        """Reorganize dataset and create annotation"""
        if not self.dataset_path:
            QMessageBox.warning(self, "Warning", "Please select a dataset folder first")
            return
            
        target_dir = QFileDialog.getExistingDirectory(self, 'Select Target Folder')
        if not target_dir:
            return
            
        org_type = self.org_type_combo.currentText()
        dataset_file = os.path.join(self.dataset_path, "dataset.csv")
        
        if not os.path.exists(dataset_file):
            QMessageBox.warning(self, "Warning", "dataset.csv not found in selected folder")
            return
            
        # Create reorganized dataset
        result_dir = create_reorganized_dataset(dataset_file, target_dir, org_type)
        
        if result_dir:
            # Create annotation for reorganized dataset
            annotation_file = os.path.join(target_dir, f"{org_type}_annotation.csv")
            success = create_annotation_file(result_dir, annotation_file)
            
            if success:
                self.log(f"Reorganized dataset created: {result_dir}")
                self.log(f"Annotation created: {annotation_file}")
                QMessageBox.information(self, "Success", 
                                      "Dataset reorganized and annotation created successfully")
            else:
                self.log(f"Failed to create annotation for reorganized dataset")
                QMessageBox.critical(self, "Error", 
                                   "Dataset reorganized but failed to create annotation")
        else:
            self.log(f"Failed to reorganize dataset")
            QMessageBox.critical(self, "Error", "Failed to reorganize dataset")
    
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
            if search_method == "Single File":
                dataset_file = os.path.join(self.dataset_path, "dataset.csv")
                rate = get_rate_single_file(search_date, dataset_file)
                
            elif search_method == "X/Y Files":
                x_file = os.path.join(self.dataset_path, "X.csv")
                y_file = os.path.join(self.dataset_path, "Y.csv")
                rate = get_rate_x_y(search_date, x_file, y_file)
                
            elif search_method == "Yearly Files":
                yearly_dir = os.path.join(self.dataset_path, "yearly_data")
                if os.path.exists(yearly_dir):
                    rate = get_rate_year_files(search_date, yearly_dir)
                else:
                    self.log("Yearly data directory not found")
                    
            elif search_method == "Weekly Files":
                weekly_dir = os.path.join(self.dataset_path, "weekly_data")
                if os.path.exists(weekly_dir):
                    rate = get_rate_week_files(search_date, weekly_dir)
                else:
                    self.log("Weekly data directory not found")
                    
            if rate is not None:
                result_text = f"Rate for {date_text}: {rate}"
                self.result_display.setText(result_text)
                self.log(f"Search successful: {result_text}")
            else:
                result_text = f"No data found for {date_text}"
                self.result_display.setText(result_text)
                self.log(f"Search failed: {result_text}")
                
        except Exception as e:
            error_text = f"Error during search: {str(e)}"
            self.result_display.setText(error_text)
            self.log(error_text)
    
    def log(self, message: str):
        """Add message to log display"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    window = CurrencyDataGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()