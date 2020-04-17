from terminaltables import AsciiTable
import sys
import requests
from language import translate as _

def fetch_data(lang):
    """
    Fetch the latest supported currencies
    :return: csv data
    """
    currency_file = "currency/Currencies.csv"
    url = "https://focusmobile-interview-materials.s3.eu-west-3.amazonaws.com/" \
          "Cheap.Stocks.Internationalization.Currencies.csv"
    try:
        # Fetch the currencies as stream data
        r = requests.get(url, stream=True)
        # Raise an exception if the request for latest currency codes failed
        r.raise_for_status()
        # Get the total size of data to be fetched
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kilobyte
        with open(currency_file, 'wb') as f:
            for data in r.iter_content(block_size):
                # Update the progress bar
                # Write the streamed data to a file
                f.write(data)
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        print(_("\nFailed to fetch supported currencies. Please check your internet connection", lang))
        print(_("Using the cached currencies file\n", lang))

    # Read the saved file
    with open(currency_file) as f:
        data = f.readlines()

    # Get the title line of the data
    data.pop(0)
    return data

def supported_currencies(lang):
    data = fetch_data(lang)
    print("\U0001F5F3 " + _(" List of all supported Currencies", lang) + "\n")
    table_data = [[_("Country", lang), _("Currency Name", lang), _("Currency Code ", lang)]]
    for line in data:
        _country, _currency_name, _currency_code = line.replace("\n", "").split(',')
        td = [_country, _currency_name, _currency_code]
        table_data.append(td)
    table = AsciiTable(table_data)

    print(table.table)
    sys.exit()



def verify_support(code, lang="en", display=True):
    """
    Verify if a currency is supported

    :param code: currency code
    :param lang: Language for display
    :param display: Print to screen or return a value
    :return: boolean of currency
    """
    code = code.upper()
    if len(code) != 3:
        print("\n\U0001F479" + _("Currency code must be a 3 letters ISO 4217 Currency Code", lang))
        sys.exit()
    data = fetch_data(lang)
    country = None
    currency_code = None
    currency_name = None
    for line in data:
        _country, _currency_name, _currency_code = line.replace("\n", "").split(',')
        # Check if any currency match the provided currency
        if code == _currency_code:
            # Update the global variables
            currency_code = _currency_code
            country = _country
            currency_name = _currency_name
            # Exit the loop if any currency match
            break
    if currency_code is None:
        print("\n\U0001F479 " + _(f"Sorry, your currency {code} is not supported yet", lang))
    else:
        if display:
            print("\n\U0001f44d " + _(f"{currency_name}({currency_code}) is supported as official currency in {country}", lang))
        else:
            return True
    sys.exit(1)
