#!/usr/bin/env python3

from . import currencylayer
from . import fixer


def convert(amount, from_currency, to_currency):
    """

    :param amount: Amount to be converted
    :param from_currency: The initial currency
    :param to_currency: The currency of the result
    :return: The converted amont
    """

    # Convert the amount currencylayer API
    success, amount = currencylayer.convert(amount, from_currency, to_currency)
    if success: return amount
    # if the conversion failed, convert using fixer API
    success, amount = fixer.convert(amount, from_currency, to_currency)
    return amount


