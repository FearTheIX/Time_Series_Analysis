@echo off
chcp 65001 >nul
title Testing - Integrated Analytics Platform
echo ===================================================
echo    Running Tests for Analytics Platform
echo ===================================================
echo.

:: Run module availability tests
echo Checking module availability...
python -c "
try:
    from currency_scrapper_v2 import CurrencyScraper
    print('✓ Lab 1: Web Scraping module available')
except ImportError as e:
    print('✗ Lab 1: Web Scraping module not available')

try:
    from data_processor import CurrencyDataProcessor
    from annotation_creator import create_annotation_file
    print('✓ Lab 3: Data Processing modules available')
except ImportError as e:
    print('✗ Lab 3: Data Processing modules not available')

try:
    from time_series_analyzer import TimeSeriesAnalyzer
    print('✓ Lab 4: Time Series module available')
except ImportError as e:
    print('✗ Lab 4: Time Series module not available')
"

echo.
echo Running basic functionality tests...
python -c "
# Test basic imports and object creation
try:
    # Test Lab 1
    try:
        from currency_scrapper_v2 import CurrencyScraper
        scraper = CurrencyScraper()
        print('✓ Lab 1: Scraper object created successfully')
    except Exception as e:
        print('✗ Lab 1: Scraper creation failed')

    # Test Lab 3  
    try:
        from data_processor import CurrencyDataProcessor
        processor = CurrencyDataProcessor()
        print('✓ Lab 3: Data processor created successfully')
    except Exception as e:
        print('✗ Lab 3: Data processor creation failed')

    # Test Lab 4
    try:
        from time_series_analyzer import TimeSeriesAnalyzer
        analyzer = TimeSeriesAnalyzer()
        print('✓ Lab 4: Time series analyzer created successfully')
    except Exception as e:
        print('✗ Lab 4: Time series analyzer creation failed')

    print('All basic tests completed!')
    
except Exception as e:
    print(f'Error during testing: {e}')
"

echo.
echo Test execution completed.
pause