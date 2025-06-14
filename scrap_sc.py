import pandas as pd
import numpy as np 

def extract_sc_deposit_rates(url):
    """
    Extracts time deposit interest rates from the Bank of China website.

    Args:
        url: The URL of the Bank of China deposit offers page.

    Returns:
        A list containing interest rates for different tenors (e.g., "3 months", "6 months") and currencies ('HKD', 'USD').
        Returns None if there's an error or no rates are found.
    """

    tables = pd.read_html(url)

    rate_table = []

    for table in tables[:-1]:

        table.columns = table.iloc[0]
        table = table.iloc[1:, :]
        rate_table.append(table)

    rate_table = pd.concat(rate_table, axis=0)
    rate_table['PREFERENTIAL INTEREST RATE (P.A.)'] = rate_table['PREFERENTIAL INTEREST RATE (P.A.)'].str.rstrip('%').astype('float') / 100.0

    return rate_table.values.tolist()

# # Example usage:
# url = "https://www.sc.com/hk/deposits/online-time-deposit/"
# deposit_rates = extract_sc_deposit_rates(url)

# if deposit_rates:
#     for currency, tenor, rate in deposit_rates:
#         print(f"\n{currency} Time Deposit Rates:")
#         print(f"  {tenor}: {rate:.4f}") # Format the rate to 4 decimal places
# else:
#     print("Could not extract deposit rates.")