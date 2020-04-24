#!/usr/bin/env python3

import argparse
import language

import currency
import stock


def main():
    # Initialize the parser with a welcome message
    welcome = "A command line interface for displaying supported currencies for Cheap Stocks, Inc"
    parser = argparse.ArgumentParser(description=welcome)

    # Add a required flag for providing currency code
    parser.add_argument('-c', '--code', required=False, help="Three digit currency code ")
    parser.add_argument('-i', '--item', required=False, help="Display price of a stock item")
    parser.add_argument('-l', '--language', required=False, default="en", help="A two digit language code to display information")
    parser.add_argument('-s', '--supported_languages', action="store_true", required=False, help="List all supported languages")
    parser.add_argument('-k', '--supported_currencies', action="store_true", required=False, help="List all supported currencies")
    args = parser.parse_args()

    # Switch to the provided currency
    _lang = args.language.lower()
    lang = language.switch(_lang)
    # List supported currencies
    supported_currencies = args.supported_currencies
    if supported_currencies:
        currency.supported_currencies(lang)
    # Ensure the provided code is 3 letters long
    supported_languages = args.supported_languages
    if supported_languages:
        language.supported_languages(lang)
    # Get currency code provided
    code = args.code
    # Get stock item provided
    item = args.item
    if item is not None:
        stock.check_item(item, code, lang)
    # Verify support of a currency
    if code is not None:
        currency.verify_support(code, lang)
    # If not flag was passed, show help message
    parser.parse_args(['-h'])


if __name__ == '__main__':
    main()
    # print(convert(10, "KES"))

