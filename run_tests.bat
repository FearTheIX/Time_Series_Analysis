@echo off
chcp 65001 >nul
title Testing - Integrated Analytics Platform
echo ===================================================
echo    Running Tests for Analytics Platform
echo ===================================================
echo.

:: Create a temporary Python script for module checking
echo Checking module availability...
(
echo try:
echo     from currency_scrapper_v2 import CurrencyScraper
echo     print('✓ Lab 1: Web Scraping module available')
echo except ImportError as e:
echo     print('✗ Lab 1: Web Scraping module not available')
echo 
echo try:
echo     from data_processor import CurrencyDataProcessor
echo     from annotation_creator import create_annotation_file
echo     print('✓ Lab 3: Data Processing modules available')
echo except ImportError as e:
echo     print('✗ Lab 3: Data Processing modules not available')
echo 
echo try:
echo     from time_series_analyzer import TimeSeriesAnalyzer
echo     print('✓ Lab 4: Time Series module available')
echo except ImportError as e:
echo     print('✗ Lab 4: Time Series module not available')
) > temp_check_modules.py

python temp_check_modules.py
del temp_check_modules.py

echo.
echo Running basic functionality tests...
(
echo # Test basic imports and object creation
echo try:
echo     # Test Lab 1
echo     try:
echo         from currency_scrapper_v2 import CurrencyScraper
echo         scraper = CurrencyScraper()
echo         print('✓ Lab 1: Scraper object created successfully')
echo     except Exception as e:
echo         print('✗ Lab 1: Scraper creation failed')
echo 
echo     # Test Lab 3  
echo     try:
echo         from data_processor import CurrencyDataProcessor
echo         processor = CurrencyDataProcessor()
echo         print('✓ Lab 3: Data processor created successfully')
echo     except Exception as e:
echo         print('✗ Lab 3: Data processor creation failed')
echo 
echo     # Test Lab 4
echo     try:
echo         from time_series_analyzer import TimeSeriesAnalyzer
echo         analyzer = TimeSeriesAnalyzer()
echo         print('✓ Lab 4: Time series analyzer created successfully')
echo     except Exception as e:
echo         print('✗ Lab 4: Time series analyzer creation failed')
echo 
echo     print('All basic tests completed!')
echo     
echo except Exception as e:
echo     print(f'Error during testing: {e}')
) > temp_basic_tests.py

python temp_basic_tests.py
del temp_basic_tests.py

echo.
echo Test execution completed.
pause