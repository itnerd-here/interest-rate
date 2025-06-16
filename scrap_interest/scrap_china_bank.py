import pandas as pd
import numpy as np 

def extract_china_bank_deposit_rates(url):
    """
    Extracts time deposit interest rates from the Bank of China website.

    Args:
        url: The URL of the Bank of China deposit offers page.

    Returns:
        A list containing interest rates for different tenors (e.g., "3 months", "6 months") and currencies ('HKD', 'USD').
        Returns None if there's an error or no rates are found.
    """

    tables = pd.read_html(url)

    # Extract HKD, USD, CNY rate
    major_currency = tables[0]

    major_cur_table = pd.melt(
        major_currency[major_currency['Integrated Account Services'].str.contains('Enrich')],
        id_vars=['Currency'],
        value_vars=['3-month', '6-month', '12-month']
        )
    
    major_cur_table.columns = ['Currency', 'tenor', 'rate']
    major_cur_table = major_cur_table[major_cur_table.rate != '-']
    
    # Extract AUD, NZD, GBP, CAD rate
    minor_currency = tables[5]
    minor_currency.columns = minor_currency.columns.droplevel([0,1])

    untagled_table_1 = pd.concat(
        [minor_currency.iloc[:, 0], pd.concat([minor_currency.iloc[:, 3] for i in range(len(minor_currency.columns[3].split('/')))], axis=1)],
        axis=1
    )
    untagled_table_1.columns = ['tenor', *minor_currency.columns[3].split('/')]

    untagled_table_2 = pd.concat(
        [minor_currency.iloc[:, 0], pd.concat([minor_currency.iloc[:, 4] for i in range(len(minor_currency.columns[4].split('/')))], axis=1)],
        axis=1
    )
    untagled_table_2.columns = ['tenor', *minor_currency.columns[4].split('/')]

    minor_cur_table = pd.merge(untagled_table_1, untagled_table_2, how='outer', on='tenor')
    minor_cur_table = pd.melt(minor_cur_table, id_vars='tenor', var_name='Currency', value_name='rate')

    rate_table = pd.concat([major_cur_table, minor_cur_table], axis=0)
    rate_table.rate = rate_table.rate.str.rstrip('%').astype('float') / 100.0
    rate_table['Currency'] = rate_table['Currency'].str.strip()

    return rate_table.values.tolist()

# # Example usage:
# url = "https://www.bochk.com/en/deposits/promotion/timedeposits.html"
# deposit_rates = extract_china_bank_deposit_rates(url)

# if deposit_rates:
#     for currency, tenor, rate in deposit_rates:
#         print(f"\n{currency} Time Deposit Rates:")
#         print(f"  {tenor}: {rate:.4f}") # Format the rate to 4 decimal places
# else:
#     print("Could not extract deposit rates.")