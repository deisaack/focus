import sys
from language import translate as _
from convert import convert

import currency

__all__ = ["check_item"]


def check_item(stock, currency_code, lang):
    """
    Check if a stock item is available and its price, we dont have data on stock and we will therefore assume all stock is
    available and all have a price of 120 USD

    :param stock: Name of the item
    :param currency_code: default USD
    :param lang: language to display
    :return: None
    """
    if currency_code is not None:
        currency.verify_support(currency_code, lang, display=False)
        currency_code = currency_code.upper()
    else:
        currency_code = "USD"

    # Since we do not have data on stocks, we give the stock a default price of 100 USD
    price = 120
    if currency_code != "USD":
        # convert the amount
        price = convert(price, from_currency="USD", to_currency=currency_code)
    print(_(f"The current price for {stock} is {price} {currency_code}", lang))
    sys.exit()
