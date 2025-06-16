from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

def extract_hang_seng_deposit_rates(url):
    """
    Extracts time deposit interest rates from the Hang Seng Bank website.

    Args:
        url: The URL of the Hang Seng Bank deposit offers page.

    Returns:
        A list containing interest rates for different tenors (e.g., "3 months", "6 months") and currencies ('HKD', 'USD').
        Returns None if there's an error or no rates are found.
    """
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(1)
        driver.close()

        rates = []

        # Find all currency from title (this might need adjustment if the site structure changes)
        titles = soup.find_all("div", class_="table-title")

        # Find all tables containing deposit rates (this might need adjustment if the site structure changes)
        rate_tables = soup.find_all("table", {"class": "ui-table"} )

        # Extract the lower tier of interest rate
        for title, rate_table in zip(titles[17:], rate_tables[17:]):
            currency_match = None
            try:
                # Extract currency from the caption (more reliable than previous methods)
                currency_match = re.search(r"([A-Z]{3})", title.text)  # Look for 3-letter currency code
                if currency_match:
                    currency = currency_match.group(1)
                else:
                    return None # Currency not found
            
                # Extract rate with corresponding tenor from table
                pattern = r"(\d+\s*months*)</td>\s*<td.*?>(.*?)</td>"
                for row in rate_table.find_all("tr"):
                    match = re.search(pattern, str(row))
                    if match:
                        month = match.group(1).strip()
                        rate_text = (match.group(2))
                        rate = float(rate_text) / 100.0  #
                        rates.append([currency, month, rate])
                    else:
                        pass
            
            except Exception as e:
                print(f"Error extracting data from table: {e}")

        return rates if rates else None  # Return None if no rates found


    except Exception as e:
        print(f"Error extracting rates: {e}")
        return None




# # Example usage:
# url = "https://cms.hangseng.com/cms/emkt/pmo/grp06/p04/eng/index.html"
# deposit_rates = extract_hang_seng_deposit_rates(url)

# if deposit_rates:
#     for currency, tenor, rate in deposit_rates:
#         print(f"\n{currency} Time Deposit Rates:")
#         print(f"  {tenor}: {rate:.4f}") # Format the rate to 4 decimal places
# else:
#     print("Could not extract deposit rates.")