#!/usr/bin/env python3

import requests

API_KEY = "0391ac8386228abaf150dd1594cbe372"


def fetch_rates():
    """
    Fetch the latest exchange rates fromfixer api

    :return:  A tuple showing if the the request was successful and the data received
    """
    url = f"http://api.currencylayer.com/live?access_key={API_KEY}"
    r = requests.get(url)
    try:
        data = r.json()
        r.raise_for_status()
    except:
        return False, None
    return True, data


def get_rate(from_currency, to_currency, data):
    """
        Get a specific exchange rate

        :param from_currency: currency of the initial amount
        :param to_currency: currency of the result
        :param data: Exchange rate data
        :return:
        """
    quotes = data["quotes"]
    if not from_currency=="USD":
        raise ValueError("From currency must be USD")
    key = f"{from_currency}{to_currency}"
    value = quotes[key]
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
    value = float(amount) * get_rate(from_currency, to_currency, data)
    return True, value
