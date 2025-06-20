from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import time

def extract_hang_seng_fx(url):
    """
    Extracts time FX rate from Hang Seng website.

    Args:
        url: The URL of the Hang Seng FX rate page.

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

    rate_table.columns = rate_table.columns.droplevel(0) 
    rate_table = rate_table.iloc[:, 1:-1]
    rate_table.columns = ['Currency Code', 'Bank Buy', 'Bank Sell']

    driver.close()
    
    return rate_table

# Example usage:
# url = "https://www.hangseng.com/en-hk/rates/foreign-currency-tt-exchange-rates"
# result = extract_hang_seng_fx(url)

# print(result)