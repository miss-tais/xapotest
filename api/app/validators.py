from .currency import currency


def currency_validator(value):
    """Function checks if value in list of available currencies"""

    value = value.upper()

    if value not in currency.currencies:
        raise ValueError("Wrong currency")

    return value


def greater_then_zero_validator(value):
    """Function checks if value is integer and greater then 0"""

    value = int(value)

    if value <= 0:
        raise ValueError("Must be greater then 0")

    return value

