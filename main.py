from scrap_interest import scrap_hsbc, scrap_hang_seng, scrap_china_bank, scrap_sc
from upload_sheet import upload_df_to_gsheet
from datetime import datetime 
import pandas as pd

# Example usage:

def main():

    today_str = datetime.today().strftime('%Y-%m-%d')
    hsbc_url = "https://www.hsbc.com.hk/accounts/offers/deposits/"
    hang_seng_url = "https://cms.hangseng.com/cms/emkt/pmo/grp06/p04/eng/index.html"
    china_bank_url = "https://www.bochk.com/en/deposits/promotion/timedeposits.html"
    sc_url = "https://www.sc.com/hk/deposits/online-time-deposit/"

    banks_name = ['HSBC', 'Hang Seng Bank', 'BoC Hong Kong', 'SC HK']
    banks_url = [hsbc_url, hang_seng_url, china_bank_url, sc_url]
    banks_func = [scrap_hsbc.extract_hsbc_deposit_rates, scrap_hang_seng.extract_hang_seng_deposit_rates, scrap_china_bank.extract_china_bank_deposit_rates, scrap_sc.extract_sc_deposit_rates]

    result = []

    for name, url, bank_func in zip(banks_name, banks_url, banks_func):

        temp = pd.DataFrame(bank_func(url), columns=['currency', 'tenor', 'rate'])
        temp['bank'] = name
        temp['date'] = today_str
        result.append(temp)

    spreadsheet_name = "Interest Rate"  
    credentials_path = "credentials.json"  # Replace with the actual path

    # Upload the DataFrame
    upload_df_to_gsheet(pd.concat(result, axis=0), spreadsheet_name, sheet_name='interest rate' ,credentials_path=credentials_path)

    pass

if __name__ == "__main__":
    main()