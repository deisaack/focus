#!/usr/bin/env python3

import requests

API_KEY = "69f9810d3e3192cb6d51a64322a681e1"


def fetch_rates():
    """
    Fetch the latest exchange rates fromfixer api

    :return:  A tuple showing if the the request was successful and the data received
    """
    url = f"http://data.fixer.io/api/latest?access_key={API_KEY}"
    r = requests.get(url)
    try:
        data = r.json()
        r.raise_for_status()
    except:
        return False, None
    return True, data


def get_rate(from_currency, data):
    """
    Get a specific exchange rate

    :param from_currency: currency of the initial amount
    :param data: Exchange rate data
    :return:
    """
    rates = data["rates"]
    key = f"{from_currency}"
    value = rates[key]
    return value


def convert(amount, from_currency, to_currency):
    """
    Perform a currency conversion
    :param amount: Value to be converted
    :param from_currency: initial currency
    :param to_currency: result currency
    :return: Tuple of whether conversion was successful or not and the converted value
    """
    success, data = fetch_rates()
    if not success:
        return False, None
    # convert the amount to euros
    value = float(amount) / get_rate(from_currency, data)
    # # Now convert to the desired currency
    value = float(value) * get_rate(to_currency, data)
    return True, value
