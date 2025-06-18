import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def upload_df_to_gsheet(df, spreadsheet_name, sheet_name="Sheet1", credentials_path="path/to/your/credentials.json"):
    """Uploads a Pandas DataFrame to a Google Sheet.

    Args:
        df: The Pandas DataFrame to upload.
        spreadsheet_name: The name of the Google Sheet (or its URL).
        sheet_name: The name of the sheet within the spreadsheet (defaults to "Sheet1").
        credentials_path: Path to your Google Cloud service account credentials JSON file.
    """
    try:
        # 1. Authenticate with Google Sheets API
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'  # Optional: If you need to create new spreadsheets
        ]
        
        gc = gspread.service_account(filename=credentials_path)


        # 2. Open or create the spreadsheet
        try:  # Try opening by name first
            sh = gc.open(spreadsheet_name)
            print('Open existing spreadsheet')
        except gspread.SpreadsheetNotFound: # If not found, create it
            sh = gc.create(spreadsheet_name)
            print('Create a new spreadsheet')


        # 3. Select or create the worksheet
        try:
            worksheet = sh.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sh.add_worksheet(title=sheet_name, rows=1000, cols=26) # Adjust rows/cols as needed
        
        # 3.5 Clear existing data in the worksheet (optional)
        # worksheet.clear()

        # 4. Convert DataFrame to a list of lists
        data = [df.columns.tolist()] + df.values.tolist()


        # 5. Upload the data
        worksheet.update(data, "B1")

        print(f"DataFrame uploaded to '{spreadsheet_name}', sheet '{sheet_name}'")


    except gspread.exceptions.APIError as e:
        print(f"Google Sheets API Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")




# # Example usage:
# # Create a sample DataFrame
# data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
# df = pd.DataFrame(data)

# # Replace with your spreadsheet name and credentials path
# spreadsheet_name = "Interest Rate"  
# credentials_path = "./interest-rate-462816-bee57e7ecb35.json"  # Replace with the actual path

# # Upload the DataFrame
# upload_df_to_gsheet(df, spreadsheet_name, credentials_path=credentials_path)