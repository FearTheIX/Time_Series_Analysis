"""
Data loading and preprocessing module
Handles CSV reading, date parsing, and basic data validation
"""

import pandas as pd
import numpy as np
from config import DATA_FILE, DATE_COLUMN, VALUE_COLUMN

class DataLoader:
    def __init__(self):
        self.data = None
        self.original_data = None
        
    def load_data(self):
        """Load dataset from CSV file and parse dates"""
        try:
            # Read CSV file
            self.original_data = pd.read_csv(DATA_FILE)
            
            # Convert date column to datetime
            self.original_data[DATE_COLUMN] = pd.to_datetime(self.original_data[DATE_COLUMN])
            
            # Set date as index for time series analysis
            self.data = self.original_data.set_index(DATE_COLUMN)
            
            # Validate data
            self._validate_data()
            
            print(f"Data loaded successfully: {len(self.data)} records")
            return self.data
            
        except FileNotFoundError:
            print(f"Error: File {DATA_FILE} not found")
            return None
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
    
    def _validate_data(self):
        """Perform basic data validation"""
        # Check for missing values
        missing_values = self.data[VALUE_COLUMN].isnull().sum()
        if missing_values > 0:
            print(f"Warning: {missing_values} missing values found")
        
        # Check for duplicates
        duplicates = self.data.index.duplicated().sum()
        if duplicates > 0:
            print(f"Warning: {duplicates} duplicate dates found")
            
        # Basic statistics
        print(f"Date range: {self.data.index.min()} to {self.data.index.max()}")
        print(f"Value range: {self.data[VALUE_COLUMN].min():.4f} to {self.data[VALUE_COLUMN].max():.4f}")
    
    def get_data_summary(self):
        """Get basic summary statistics of the data"""
        if self.data is None:
            return None
            
        summary = {
            'total_records': len(self.data),
            'date_range': (self.data.index.min(), self.data.index.max()),
            'value_stats': self.data[VALUE_COLUMN].describe().to_dict(),
            'missing_values': self.data[VALUE_COLUMN].isnull().sum()
        }
        return summary

# Example usage
if __name__ == "__main__":
    loader = DataLoader()
    data = loader.load_data()
    if data is not None:
        summary = loader.get_data_summary()
        print("\nData Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")