import requests


class Currency:
    """Class currency stores list of available currencies in ISO3 format"""

    def __init__(self):
        self.__currencies = []

        resp = requests.get('https://openexchangerates.org/api/currencies.json')

        if resp.status_code == requests.codes.ok:
            self.__currencies.extend(resp.json().keys())

    @property
    def currencies(self):
        return self.__currencies


currency = Currency()
