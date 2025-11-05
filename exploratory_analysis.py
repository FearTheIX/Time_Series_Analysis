"""
Exploratory Data Analysis (EDA) for time series data
Includes visualization and statistical analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from config import VALUE_COLUMN

class ExploratoryAnalysis:
    def __init__(self, data):
        self.data = data
        self.setup_plot_style()
    
    def setup_plot_style(self):
        """Setup consistent plotting style"""
        plt.style.use('seaborn-v0_8')
        self.colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
        
    def plot_time_series(self, save_path=None):
        """Plot the complete time series"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Exchange Rate Time Series Analysis', fontsize=16, fontweight='bold')
        
        # Main time series plot
        axes[0, 0].plot(self.data.index, self.data[VALUE_COLUMN], 
                       color=self.colors[0], linewidth=1)
        axes[0, 0].set_title('Complete Time Series')
        axes[0, 0].set_ylabel('Exchange Rate')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Yearly subsets to show different periods
        years_to_show = [(1998, 1999), (2008, 2009), (2015, 2017)]
        for idx, (start_year, end_year) in enumerate(years_to_show):
            mask = (self.data.index.year >= start_year) & (self.data.index.year <= end_year)
            subset_data = self.data[mask]
            
            row = (idx + 1) // 2
            col = (idx + 1) % 2
            if row < 2 and col < 2:
                axes[row, col].plot(subset_data.index, subset_data[VALUE_COLUMN], 
                                  color=self.colors[idx + 1], linewidth=1.5)
                axes[row, col].set_title(f'Time Series {start_year}-{end_year}')
                axes[row, col].set_ylabel('Exchange Rate')
                axes[row, col].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_distribution(self, save_path=None):
        """Plot distribution of exchange rates"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Histogram with KDE
        axes[0].hist(self.data[VALUE_COLUMN], bins=50, alpha=0.7, 
                    color=self.colors[0], edgecolor='black')
        axes[0].set_title('Distribution of Exchange Rates')
        axes[0].set_xlabel('Exchange Rate')
        axes[0].set_ylabel('Frequency')
        axes[0].grid(True, alpha=0.3)
        
        # Box plot
        axes[1].boxplot(self.data[VALUE_COLUMN])
        axes[1].set_title('Box Plot of Exchange Rates')
        axes[1].set_ylabel('Exchange Rate')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_summary_statistics(self):
        """Generate comprehensive summary statistics"""
        stats = {
            'Basic Statistics': self.data[VALUE_COLUMN].describe(),
            'Volatility Metrics': {
                'Variance': self.data[VALUE_COLUMN].var(),
                'Standard Deviation': self.data[VALUE_COLUMN].std(),
                'Coefficient of Variation': self.data[VALUE_COLUMN].std() / self.data[VALUE_COLUMN].mean()
            },
            'Distribution Metrics': {
                'Skewness': self.data[VALUE_COLUMN].skew(),
                'Kurtosis': self.data[VALUE_COLUMN].kurtosis()
            }
        }
        return stats

# Example usage
if __name__ == "__main__":
    from data_loader import DataLoader
    
    loader = DataLoader()
    data = loader.load_data()
    
    if data is not None:
        explorer = ExploratoryAnalysis(data)
        explorer.plot_time_series('time_series_plot.png')
        explorer.plot_distribution('distribution_plot.png')
        
        stats = explorer.generate_summary_statistics()
        print("\nSummary Statistics:")
        for category, values in stats.items():
            print(f"\n{category}:")
            if isinstance(values, dict):
                for key, value in values.items():
                    print(f"  {key}: {value:.4f}")
            else:
                print(values)