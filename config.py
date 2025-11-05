"""
Configuration file for time series analysis project
Contains all constants and settings
"""

# Data file configuration
DATA_FILE = 'dataset.csv'
DATE_COLUMN = 'date'
VALUE_COLUMN = 'rate'

# Analysis parameters
TEST_SIZE = 0.2  # 20% for testing
RANDOM_STATE = 42

# Model parameters
FORECAST_STEPS = 30