"""
Lead Generation Web Scraper
Collects NGO/Organization data from public sources
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime


url = "https://thenationaltrust.in/content/registered_organization.php"


def scrape_data(target_url):
    """
    Scrape organization data from target URL
    
    Args:
        target_url (str): URL to scrape data from
    
    Returns:
        pd.DataFrame: Scraped data as dataframe
    """
    try:
        print(f"Fetching data from: {target_url}")
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(target_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Error: Access denied or page not found. Status: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find table
        table = soup.find('table')
        if table is None:
            print("Error: No table found on the page.")
            return None
        
        rows = table.find_all('tr')
        print(f"Found {len(rows) - 1} data rows")
        
        # Extract headers from first row
        headers_list = []
        if len(rows) > 0:
            header_cols = rows[0].find_all('th')
            if header_cols:
                headers_list = [ele.text.strip() for ele in header_cols]
            else:
                # If no <th>, use first row as headers
                header_cols = rows[0].find_all('td')
                headers_list = [ele.text.strip() for ele in header_cols]
        
        # Extract data
        data = []
        for row in rows[1:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if cols:  # Only add non-empty rows
                data.append(cols)
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=headers_list if headers_list else None)
        
        # Save to CSV
        filename = 'scraped_data.csv'
        df.to_csv(filename, index=False)
        
        print(f"✓ Data successfully saved to {filename}")
        print(f"✓ Total records: {len(data)}")
        print(f"✓ Columns: {', '.join(headers_list)}")
        print(f"✓ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {str(e)}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error scraping data: {str(e)}", file=sys.stderr)
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("Lead Generation Web Scraper")
    print("=" * 50)
    scrape_data(url)
    print("=" * 50)
