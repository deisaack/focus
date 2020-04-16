#!/usr/bin/env python

import argparse, requests
from tqdm import tqdm

# Global variables
country = None
currency_code = None
currency_name = None
currency_file = "Currencies.csv"
url = "https://focusmobile-interview-materials.s3.eu-west-3.amazonaws.com/Cheap.Stocks.Internationalization.Currencies.csv"

# Initialize the parser with a welcome message
welcome = "A command line interface for displaying supported currencies for Cheap Stocks, Inc"
parser = argparse.ArgumentParser(description=welcome)

# Add a required flag for providing currency code
parser.add_argument('-c', '--code', required=True, help="Three digit currency code ")
args = parser.parse_args()

# Store the supplied currency code
code = args.code.upper()

# Ensure the provided code is 3 letters long
if len(code) != 3:
    raise ValueError("Currency code must be a 3 letters ISO 4217 Currency Code")
try:
    # Fetch the currencies as stream data
    r = requests.get(url, stream=True)
    # Raise an exception if an the request for latest currency codes failed
    r.raise_for_status()
    # Get the total size of data to be fetched
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kilobyte

    print("\nFetching the latest Currency codes \r\n")
    # Initialize tqdm for showing the progress bar
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(currency_file, 'wb') as f:
        for data in r.iter_content(block_size):
            # Update the progress bar
            t.update(len(data))
            # Write the streamed data to a file
            f.write(data)
    t.close()
    # Check to ensure some data was received
    if total_size != 0 and t.n != total_size:
        print("ERROR, something went wrong")
    else:
        print("\n")
except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
    print("\nFailed to fetch supported currencies. Please check your internet connection\r\n")
    print("Using the cached currencies file\n")

# Read the saved file
with open(currency_file) as f:
    data = f.readlines()

# Get the title line of the data
title = data.pop(0)

# Process each line of the csv
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
    print("\U0001F479 Sorry, your currency {0} is not supported yet\n".format(code))
else:
    print("\U0001f44d {0}({1}) is supported as official currency in {2}\n".format(currency_name, currency_code, country))
