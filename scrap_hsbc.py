import requests
from bs4 import BeautifulSoup
import re

def extract_hsbc_deposit_rates(url):
    """
    Extracts time deposit interest rates from the HSBC HK website.

    Args:
        url: The URL of the HSBC HK deposit offers page.

    Returns:
        A dictionary where keys are currencies (e.g., "HKD", "USD") and values
        are dictionaries containing interest rates for different tenors (e.g., "3 months", "6 months").
        Returns None if there's an error or no rates are found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        rates = []

        # Find all tables containing deposit rates (this might need adjustment if the site structure changes)
        rate_tables = soup.find_all("table", {"class": "desktop"} )


        for table in rate_tables[2:49:8]:
            # Extract currency from table header or nearby text (this is the tricky part and highly site-specific)
            currency_match = None
            try:
                # Extract currency from the caption (more reliable than previous methods)
                caption = table.find("caption")
                if caption:
                    currency_match = re.search(r"([A-Z]{3})", caption.text)  # Look for 3-letter currency code
                    if currency_match:
                        currency = currency_match.group(1)
                    else:
                        return None # Currency not found
            except Exception as e:
                print(f"Error extracting data from table: {e}")
                return None

            # Extract rate with corresponding tenor from table
            pattern = r'<span class="A-PAR16R-RW-ALL">(.*?)</span>'
            for row in table.find_all("tr")[1:]:  # Skip header row
                matches = re.findall(pattern, str(row))
                if len(matches) >= 2:
                    month, rate_text = matches[0].partition('months')[0]+'months', matches[1].partition('%')[0]+'%'
                    rate = float(rate_text.replace("%", "")) / 100.0  #
                    rates.append([currency, month, rate])
                else:
                    print("Could not extract both month and rate.")

        return rates if rates else None  # Return None if no rates found


    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error extracting rates: {e}")
        return None




# Example usage:
url = "https://www.hsbc.com.hk/accounts/offers/deposits/"
deposit_rates = extract_hsbc_deposit_rates(url)

if deposit_rates:
    for currency, tenor, rate in deposit_rates:
        print(f"\n{currency} Time Deposit Rates:")
        print(f"  {tenor}: {rate:.4f}") # Format the rate to 4 decimal places
else:
    print("Could not extract deposit rates.")