"""
Adapter for Laboratory Work 2 data analysis functionality
Provides unified interface for data analysis operations
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


class DataAnalyzer:
    """
    Data analysis adapter for Lab 2 functionality
    Provides statistical analysis and data processing methods
    """
    
    def __init__(self):
        """Initialize the data analyzer"""
        self.current_data = None
        self.analysis_results = {}
    
    def load_data(self, filepath):
        """
        Load dataset from file
        
        Args:
            filepath (str): Path to data file
            
        Returns:
            pandas.DataFrame: Loaded data
        """
        try:
            if filepath.endswith('.csv'):
                self.current_data = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                self.current_data = pd.read_excel(filepath)
            else:
                raise ValueError("Unsupported file format")
            
            print(f"Data loaded successfully: {filepath}")
            print(f"Data shape: {self.current_data.shape}")
            
            return self.current_data
            
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_basic_statistics(self, df=None):
        """
        Generate basic statistics for the dataset
        
        Args:
            df (pandas.DataFrame, optional): Data to analyze
            
        Returns:
            dict: Statistical summary
        """
        data = df if df is not None else self.current_data
        
        if data is None:
            raise ValueError("No data available for analysis")
        
        stats_summary = {
            'shape': data.shape,
            'columns': list(data.columns),
            'data_types': data.dtypes.to_dict(),
            'missing_values': data.isnull().sum().to_dict(),
            'basic_stats': data.describe().to_dict(),
            'numeric_columns': data.select_dtypes(include=[np.number]).columns.tolist()
        }
        
        return stats_summary
    
    def detect_outliers(self, column):
        """
        Detect outliers in specified column using IQR method
        
        Args:
            column (str): Column name to analyze
            
        Returns:
            dict: Outlier information
        """
        if self.current_data is None:
            raise ValueError("No data available for analysis")
        
        if column not in self.current_data.columns:
            raise ValueError(f"Column '{column}' not found in data")
        
        series = self.current_data[column].dropna()
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        
        outlier_info = {
            'column': column,
            'total_values': len(series),
            'outlier_count': len(outliers),
            'outlier_percentage': (len(outliers) / len(series)) * 100,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers': outliers.tolist()
        }
        
        return outlier_info
    
    def generate_report(self, df=None):
        """
        Generate comprehensive analysis report
        
        Args:
            df (pandas.DataFrame, optional): Data to analyze
            
        Returns:
            str: Formatted report string
        """
        data = df if df is not None else self.current_data
        
        if data is None:
            return "No data available for report generation"
        
        report = []
        report.append("=== COMPREHENSIVE DATA ANALYSIS REPORT ===")
        report.append(f"Dataset Shape: {data.shape}")
        report.append(f"Columns: {', '.join(data.columns)}")
        
        report.append("\n=== DATA TYPES ===")
        for col, dtype in data.dtypes.items():
            report.append(f"  {col}: {dtype}")
        
        report.append("\n=== MISSING VALUES ===")
        missing_values = data.isnull().sum()
        for col, missing in missing_values.items():
            report.append(f"  {col}: {missing} ({missing/len(data)*100:.2f}%)")
        
        report.append("\n=== BASIC STATISTICS ===")
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats_df = data[numeric_cols].describe()
            report.append(stats_df.to_string())
        else:
            report.append("No numeric columns for statistical analysis")
        
        report.append("\n=== OUTLIER ANALYSIS ===")
        for col in numeric_cols:
            outlier_info = self.detect_outliers(col)
            report.append(f"  {col}: {outlier_info['outlier_count']} outliers ({outlier_info['outlier_percentage']:.2f}%)")
        
        return "\n".join(report)
    
    def filter_by_threshold(self, column, threshold, keep_above=True):
        """
        Filter data based on threshold value
        
        Args:
            column (str): Column to filter
            threshold (float): Threshold value
            keep_above (bool): Whether to keep values above threshold
            
        Returns:
            pandas.DataFrame: Filtered data
        """
        if self.current_data is None:
            raise ValueError("No data available for filtering")
        
        if column not in self.current_data.columns:
            raise ValueError(f"Column '{column}' not found")
        
        if keep_above:
            filtered_data = self.current_data[self.current_data[column] >= threshold]
        else:
            filtered_data = self.current_data[self.current_data[column] < threshold]
        
        return filtered_data


# Example usage and testing
if __name__ == "__main__":
    """Test the data analyzer"""
    analyzer = DataAnalyzer()
    
    try:
        # Load sample data
        data = analyzer.load_data('dataset.csv')
        
        # Generate statistics
        stats = analyzer.get_basic_statistics()
        print("Basic statistics generated")
        
        # Generate report
        report = analyzer.generate_report()
        print(report)
        
    except Exception as e:
        print(f"Error in data analysis: {e}")