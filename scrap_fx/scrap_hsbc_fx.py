from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import time

def extract_hsbc_fx(url):
    """
    Extracts time FX rate from HSBC website.

    Args:
        url: The URL of the HSBC FX rate page.

    Returns:
        A list containing interest rates for different currencies ('HKD', 'USD').
        Returns None if there's an error or no rates are found.
    """

    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rate_tables = soup.find_all("table")

    rate_table = pd.read_html(str(rate_tables))[0]

    currency_code_map = {
        "US Dollar": "USD",
        "Australian Dollar": "AUD",
        "Canadian Dollar": "CAD",
        "Euro": "EUR",
        "Japanese Yen": "JPY",
        "New Zealand Dollar": "NZD",
        "Pound Sterling": "GBP",
        "Renminbi": "RMB",
        "Singapore Dollar": "SGD",
        "Swiss Franc": "CHF",
        "Thai Baht": "THB"
    }

    rate_table = rate_table.iloc[:, :3]
    rate_table['Currency Code'] = rate_table['Currency'].str.split('view').str[0].map(currency_code_map)
    rate_table = rate_table.iloc[:, 1:]
    rate_table.columns = ['Bank Buy', 'Bank Sell', 'Currency Code']

    driver.close()

    return rate_table

# # Example usage:
# url = "https://www.hsbc.com.hk/investments/products/foreign-exchange/currency-rate/"
# deposit_rates = extract_hsbc_fx(url)

# print(deposit_rates)