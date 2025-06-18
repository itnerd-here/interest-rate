from scrap_interest import scrap_hsbc, scrap_hang_seng, scrap_china_bank, scrap_sc
from scrap_fx import scrap_hsbc_fx, scrap_hang_seng_fx, scrap_boc_fx
from upload_sheet import upload_df_to_gsheet
from datetime import datetime 
import pandas as pd
import time

# Example usage:

def main():

    spreadsheet_name = "Interest Rate"  
    credentials_path = "credentials.json"  # Replace with the actual path

    today_str = datetime.today().strftime('%Y-%m-%d')

    # Create deposit df
    print('Start extracting deposit data')
    
    hsbc_url = "https://www.hsbc.com.hk/accounts/offers/deposits/"
    hang_seng_url = "https://cms.hangseng.com/cms/emkt/pmo/grp06/p04/eng/index.html"
    china_bank_url = "https://www.bochk.com/en/deposits/promotion/timedeposits.html"
    sc_url = "https://www.sc.com/hk/deposits/online-time-deposit/"

    banks_name = ['HSBC', 'Hang Seng Bank', 'BoC Hong Kong', 'SC HK']
    banks_url = [hsbc_url, hang_seng_url, china_bank_url, sc_url]
    banks_func = [scrap_hsbc.extract_hsbc_deposit_rates, scrap_hang_seng.extract_hang_seng_deposit_rates, scrap_china_bank.extract_china_bank_deposit_rates, scrap_sc.extract_sc_deposit_rates]

    deposit_result = []

    for name, url, bank_func in zip(banks_name, banks_url, banks_func):

        temp = pd.DataFrame(bank_func(url), columns=['Currency Code', 'Tenor', 'Rate'])
        temp['Bank'] = name
        temp['Date'] = today_str
        deposit_result.append(temp)

    deposit_result = pd.concat(deposit_result, axis=0)
    deposit_result = deposit_result.loc[:, ['Currency Code', 'Bank', 'Date', 'Tenor', 'Rate']]

    # Upload the dataframe
    upload_df_to_gsheet(deposit_result, spreadsheet_name, sheet_name='interest rate' ,credentials_path=credentials_path)
    print('Uploaded to interest rate')

    # Create fx df
    print('Start extracting FX data')

    hsbc_fx_url = "https://www.hsbc.com.hk/investments/products/foreign-exchange/currency-rate/"
    hang_seng_fx_url = "https://www.hangseng.com/en-hk/rates/foreign-currency-tt-exchange-rates"
    boc_fx_url = "https://www.bochk.com/whk/rates/exchangeRatesHKD/exchangeRatesHKD-input.action?lang=en"

    banks_fx_name = ['HSBC', 'Hang Seng Bank', 'BoC Hong Kong']
    banks_fx_url = [hsbc_fx_url, hang_seng_fx_url, boc_fx_url]
    banks_fx_func = [scrap_hsbc_fx.extract_hsbc_fx, scrap_hang_seng_fx.extract_hang_seng_fx, scrap_boc_fx.extract_boc_fx]

    fx_result = []

    for name, url, bank_func in zip(banks_fx_name, banks_fx_url, banks_fx_func):
        
        temp = bank_func(url)
        temp['Bank'] = name
        temp['Date'] = today_str
        fx_result.append(temp)
        time.sleep(3)
    fx_result = pd.concat(fx_result, axis=0)
    fx_result = fx_result.loc[:, ['Currency Code', 'Bank', 'Date', 'Bank Buy', 'Bank Sell']]

    sc_fx = fx_result.groupby('Currency Code')[['Bank Buy', 'Bank Sell']].mean().reset_index()
    sc_fx['Bank']  = 'SC HK'
    sc_fx['Date'] = today_str 
    fx_result= pd.concat([fx_result, sc_fx], axis=0)
    

    # Upload the DataFrame
    upload_df_to_gsheet(fx_result, spreadsheet_name, sheet_name='fx rate' ,credentials_path=credentials_path)
    print('Uploaded to fx rate')

    pass

if __name__ == "__main__":
    main()