"""
Data processing module for currency data operations
"""

import pandas as pd
import os
import datetime
from typing import List, Optional, Tuple
import csv


class CurrencyDataProcessor:
    """Class for processing currency data from Laboratory Work 1"""
    
    def __init__(self, data_file: str = "dataset.csv"):
        """
        Initialize CurrencyDataProcessor
        
        Args:
            data_file: Path to CSV file with currency data
        """
        self.data_file = data_file
        self.df = self._load_data()
    
    def _load_data(self) -> pd.DataFrame:
        """
        Load currency data from CSV file
        
        Returns:
            DataFrame with currency data
        """
        try:
            df = pd.read_csv(self.data_file)
            # Ensure date is in ISO 8601 format
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            return df
        except FileNotFoundError:
            print(f"File {self.data_file} not found. Please run scraper first.")
            return pd.DataFrame()
    
    def split_to_x_y(self, x_file: str = "X.csv", y_file: str = "Y.csv") -> bool:
        """
        Split dataset into X.csv (dates) and Y.csv (rates)
        
        Args:
            x_file: Output file for dates
            y_file: Output file for rates
            
        Returns:
            True if successful
        """
        if self.df.empty:
            print("No data available")
            return False
        
        try:
            # Save dates to X.csv
            self.df[['date']].to_csv(x_file, index=False)
            # Save rates to Y.csv
            self.df[['rate']].to_csv(y_file, index=False)
            
            print(f"Successfully split data into {x_file} and {y_file}")
            return True
        except Exception as e:
            print(f"Error splitting data: {e}")
            return False
    
    def split_by_years(self, output_dir: str = "yearly_data") -> List[str]:
        """
        Split dataset by years into separate files
        
        Args:
            output_dir: Directory to save yearly files
            
        Returns:
            List of created files
        """
        if self.df.empty:
            print("No data available")
            return []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        created_files = []
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        for year, group in self.df.groupby(self.df['date'].dt.year):
            if not group.empty:
                # Get first and last date in the group
                start_date = group['date'].min().strftime("%Y%m%d")
                end_date = group['date'].max().strftime("%Y%m%d")
                
                filename = f"{start_date}_{end_date}.csv"
                filepath = os.path.join(output_dir, filename)
                
                group.to_csv(filepath, index=False)
                created_files.append(filepath)
        
        return created_files
    
    def split_by_weeks(self, output_dir: str = "weekly_data") -> List[str]:
        """
        Split dataset by weeks into separate files
        
        Args:
            output_dir: Directory to save weekly files
            
        Returns:
            List of created files
        """
        if self.df.empty:
            print("No data available")
            return []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        created_files = []
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['year_week'] = self.df['date'].dt.strftime('%Y-%U')
        
        for week, group in self.df.groupby('year_week'):
            if not group.empty:
                # Get first and last date in the group
                start_date = group['date'].min().strftime("%Y%m%d")
                end_date = group['date'].max().strftime("%Y%m%d")
                
                filename = f"{start_date}_{end_date}.csv"
                filepath = os.path.join(output_dir, filename)
                
                # Remove temporary column before saving
                group.drop('year_week', axis=1).to_csv(filepath, index=False)
                created_files.append(filepath)
        
        return created_files


def get_rate_single_file(date: datetime.datetime, filename: str = "dataset.csv") -> Optional[float]:
    """
    Search for currency rate in single file
    
    Args:
        date: Date to search for
        filename: CSV file to search in
        
    Returns:
        Currency rate or None if not found
    """
    try:
        df = pd.read_csv(filename)
        df['date'] = pd.to_datetime(df['date'])
        date_str = date.strftime('%Y-%m-%d')
        
        result = df[df['date'] == date]
        return result['rate'].iloc[0] if not result.empty else None
    except Exception as e:
        print(f"Error searching in single file: {e}")
        return None


def get_rate_x_y(date: datetime.datetime, x_file: str = "X.csv", y_file: str = "Y.csv") -> Optional[float]:
    """
    Search for currency rate in separated X and Y files
    
    Args:
        date: Date to search for
        x_file: File with dates
        y_file: File with rates
        
    Returns:
        Currency rate or None if not found
    """
    try:
        dates_df = pd.read_csv(x_file)
        rates_df = pd.read_csv(y_file)
        
        date_str = date.strftime('%Y-%m-%d')
        mask = dates_df['date'] == date_str
        
        if mask.any():
            index = mask.idxmax()
            return rates_df.iloc[index]['rate']
        return None
    except Exception as e:
        print(f"Error searching in X/Y files: {e}")
        return None


def get_rate_year_files(date: datetime.datetime, data_dir: str = "yearly_data") -> Optional[float]:
    """
    Search for currency rate in yearly split files
    
    Args:
        date: Date to search for
        data_dir: Directory with yearly files
        
    Returns:
        Currency rate or None if not found
    """
    try:
        year = date.year
        pattern = f"{year}*.csv"
        
        for file in os.listdir(data_dir):
            if file.startswith(str(year)):
                filepath = os.path.join(data_dir, file)
                df = pd.read_csv(filepath)
                df['date'] = pd.to_datetime(df['date'])
                
                date_str = date.strftime('%Y-%m-%d')
                result = df[df['date'] == date]
                
                if not result.empty:
                    return result['rate'].iloc[0]
        return None
    except Exception as e:
        print(f"Error searching in yearly files: {e}")
        return None


def get_rate_week_files(date: datetime.datetime, data_dir: str = "weekly_data") -> Optional[float]:
    """
    Search for currency rate in weekly split files
    
    Args:
        date: Date to search for
        data_dir: Directory with weekly files
        
    Returns:
        Currency rate or None if not found
    """
    try:
        date_str_search = date.strftime('%Y%m%d')
        
        for file in os.listdir(data_dir):
            start_str, end_str = file.replace('.csv', '').split('_')
            start_date = datetime.datetime.strptime(start_str, '%Y%m%d')
            end_date = datetime.datetime.strptime(end_str, '%Y%m%d')
            
            if start_date <= date <= end_date:
                filepath = os.path.join(data_dir, file)
                df = pd.read_csv(filepath)
                df['date'] = pd.to_datetime(df['date'])
                
                date_str = date.strftime('%Y-%m-%d')
                result = df[df['date'] == date]
                
                if not result.empty:
                    return result['rate'].iloc[0]
        return None
    except Exception as e:
        print(f"Error searching in weekly files: {e}")
        return None


def create_dataset_from_files(files: List[str]) -> pd.DataFrame:
    """
    Create dataset from multiple files
    
    Args:
        files: List of CSV files to combine
        
    Returns:
        Combined DataFrame
    """
    if isinstance(files, str):
        files = [files]
    
    dfs = []
    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            dfs.append(df)
    
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df['date'] = pd.to_datetime(combined_df['date'])
        combined_df = combined_df.sort_values('date').drop_duplicates()
        return combined_df
    else:
        return pd.DataFrame()


if __name__ == "__main__":
    """Test data processor functionality"""
    processor = CurrencyDataProcessor()
    
    if not processor.df.empty:
        print(f"Loaded dataset with {len(processor.df)} rows")
        processor.split_to_x_y()
        processor.split_by_years()
        processor.split_by_weeks()
        
        # Test date search
        test_date = datetime.datetime(2023, 6, 15)
        rate = get_rate_single_file(test_date)
        print(f"Rate for {test_date.date()}: {rate}")