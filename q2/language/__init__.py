#!/usr/bin/env python3

import requests
import sys

from terminaltables import AsciiTable

from language.translateor import *

_ = translate


def fetch_data():
    """
    Fetch the latest supported languages
    :return: csv data
    """
    language_file = "language/Languages.csv"
    url = "https://focusmobile-interview-materials.s3.eu-west-3.amazonaws.com/Cheap.Stocks.Internationalization.Languages.csv"
    try:
        # Fetch the languages as stream data
        r = requests.get(url, stream=True)
        # Raise an exception if an the request for latest languages failed
        r.raise_for_status()
        # Get the total size of data to be fetched
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kilobyte
        with open(language_file, 'wb') as f:
            for data in r.iter_content(block_size):
                # Update the progress bar
                # Write the streamed data to a file
                f.write(data)
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
        print("\nFailed to fetch supported languages. Please check your internet connection\r\n")
        print("Using the cached languages file\n")

    # Read the saved file
    with open(language_file) as f:
        data = f.readlines()

    # Get the title line of the data
    data.pop(0)
    return data


def switch(code):

    """
    Process each line of the csv and check if the currency code provided is included

    :param code: currency code provided in as a flag
    :return: language code
    """
    if code == "en":
        return code
    language = None
    language_code = None
    data = fetch_data()
    for line in data:
        _language, _language_code = line.replace("\n", "").split(',')
        # Check if any currency match the provided currency
        if code == _language_code:
            # Update the global variables
            language = _language
            language_code = _language_code
            # Exit the loop if any language match
            break
    if language_code is None:
        print("\U0001F479 Sorry, the language supplied is not supported\n")
        sys.exit()
    else:
        print("\U0001f44d Changing language to {0}\n".format(language))
    return language_code

def supported_languages(lang):
    """
    List all supported languages
    :param lang: Language to display the data
    :return: None
    """
    data = fetch_data()
    table_data = [[_("Language", lang), _("Code", lang)]]
    for line in data:
        _language, _language_code = line.replace("\n", "").split(',')
        td = [_(_language, lang), _language_code]
        table_data.append(td)
    print("\U0001F5F3 " + _(" List of all supported Currencies", lang) + "\n")
    table = AsciiTable(table_data)

    print(table.table)
    sys.exit()
