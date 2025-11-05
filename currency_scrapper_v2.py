"""
Laboratory work: Automatic data collection. Web-scraping.
"""

import requests
import csv
import datetime
from time import sleep
import random


class CurrencyScraper:
    """Class for currency data collection."""
    
    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru/archive"
        # Increase timeout for slow requests
        self.timeout = 30
        # Max retries for one day
        self.max_retries = 3
    
    def get_currency_rate(self, date):
        """Get the dollar exchange rate for a specific date with repetitive attempts."""
        date_str = date.strftime("%Y/%m/%d")
        url = f"{self.base_url}/{date_str}/daily_json.js"
        
        # Several tries with exponential backoff
        for attempt in range(self.max_retries):
            try:
                # Random delay between 0.05 and 0.15 seconds
                sleep(0.05 + random.uniform(0, 0.1))
                
                # Increase the timeout for each request
                response = requests.get(url, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    usd_rate = data['Valute']['USD']['Value']
                    print(f"Successfully received rate for {date_str}: {usd_rate}")
                    return (date.strftime("%Y-%m-%d"), usd_rate)
                else:
                    # If the page is not found (404) - there is no data > won't try again
                    if response.status_code == 404:
                        print(f"No data for {date_str} (404)")
                        return None
                    else:
                        print(f"Error {response.status_code} for {date_str}, attempt {attempt + 1}")
                        
            except requests.exceptions.Timeout:
                print(f"Timeput for {date_str}, attempt {attempt + 1}")
            except requests.exceptions.ConnectionError:
                print(f"Connection error for {date_str}, attempt{attempt + 1}")
                # Wait longer if there're connection problems.
                sleep(2)
            except Exception as e:
                print(f"Error for {date_str}: {e}, attempt {attempt + 1}")
            
            # Increase the delay before the next attempt
            if attempt < self.max_retries - 1:
                sleep(2 ** attempt)  # Exponential delay: 1, 2, 4 seconds
        
        print(f"Couldn't get data for' {date_str} after {self.max_retries} attempts")
        return None
    
    def scrape_data(self, start_year=1997):
        """The main method of data collection."""
        print("Data collection begins...")
        
        start_date = datetime.date(start_year, 1, 1)
        end_date = datetime.date.today()
        current_date = start_date
        results = []
        errors = 0
        
        total_days = (end_date - start_date).days + 1
        print(f"Total days to process: {total_days}")
        
        while current_date <= end_date:
            # Skip weekends (no data usually)
            # if current_date.weekday() >= 5:  # 5 � 6 - saturday and sunday
            #     current_date += datetime.timedelta(days=1)
            #     continue
            
            result = self.get_currency_rate(current_date)
            if result:
                results.append(result)
            else:
                errors += 1
            
            # Progress every 100 days
            processed_days = (current_date - start_date).days + 1
            if processed_days % 100 == 0:
                success_rate = (len(results) / processed_days) * 100
                print(f"Processed: {processed_days}/{total_days} days, "
                      f"success: {len(results)}, errors: {errors}, "
                      f"success rate: {success_rate:.1f}%")
            
            current_date += datetime.timedelta(days=1)
        
        print(f"Data collection end. Success: {len(results)} entries, Errors: {errors}")
        return results
    
    def save_to_csv(self, data, filename="dataset.csv"):
        """Save data to a CSV-file."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['date', 'rate'])
                writer.writerows(data)
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Saving error: {e}")
            return False
    
    def resume_from_date(self, last_successful_date, filename="dataset.csv"):
        """Continue collecting data from a specific date."""
        try:
            # Read existing data
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_data = list(reader)[1:]  # Skip title
            
            # Get the latest date from a file
            if existing_data:
                last_date = existing_data[-1][0]
                print(f"Continue collecting data from: {last_date}")
            
            # �ollect data from the last successful date
            start_date = datetime.datetime.strptime(last_successful_date, "%Y-%m-%d").date()
            new_data = self.scrape_data(start_date.year)
            
            # Combine data
            all_data = existing_data + new_data
            
            # Save
            self.save_to_csv(all_data, filename)
            print("Data successfully supplemented!")
            
        except Exception as e:
            print(f"Continuing collection error: {e}")


def main():
    """The main function of the program."""
    scraper = CurrencyScraper()
    
    # Can start at a later date for the test
    # start_year = 2020  # instead of 1997
    
    print("Start dollar exchange rate data collection...")
    currency_data = scraper.scrape_data()  # start_year=start_year ��� �����
    
    if currency_data:
        success = scraper.save_to_csv(currency_data)
        if success:
            print(f"Successfully collected {len(currency_data)} entries")
        else:
            print("Data saving error")
    else:
        print("Data collection failed")


if __name__ == "__main__":
    main()