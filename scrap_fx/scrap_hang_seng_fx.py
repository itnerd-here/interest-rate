from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

def extract_china_bank_deposit_rates(url):
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

    soup = BeautifulSoup(driver.page_source, "html.parser")
    rate_tables = soup.find_all("table")

    rate_table = pd.read_html(str(rate_tables))[0]

    rate_table.columns = rate_table.columns.droplevel(0) 
    rate_table = rate_table.iloc[:, 1:-1]
    rate_table.columns = ['Currency Code', 'Bank Buy', 'Bank Sell']

    driver.close()

    return rate_table.values.tolist()

# # Example usage:
# url = "https://www.hangseng.com/en-hk/rates/foreign-currency-tt-exchange-rates"
# deposit_rates = extract_china_bank_deposit_rates(url)

# if deposit_rates:
#     for currency, tenor, rate in deposit_rates:
#         print(f"\n{currency} Time Deposit Rates:")
#         print(f"  {tenor}: {rate:.4f}") # Format the rate to 4 decimal places
# else:
#     print("Could not extract deposit rates.")