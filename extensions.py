import json
import requests
from Config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Ошибка! Невозможно использовать одинаковый вид валюты! {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Ошибка! Невозможно обработать введенные данные! {quote}. Введите правильные данные!')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Ошибка! Невозможно обработать введенные данные! {base}. Введите правильные данные! ')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Ошибка! Введите корректную сумму! {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
