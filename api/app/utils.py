from decimal import Decimal, ROUND_HALF_UP


def calculate_price(amount, rate, digits):
    if digits < 0:
        raise ValueError('Invalid number of digits')
    elif digits == 0:
        cents = Decimal('0')
    else:
        cents = '0.{}1'.format('0' * (digits - 1))
        cents = Decimal(cents)

    exchange_amount = Decimal(amount)
    exchange_rate = Decimal(rate)
    exchange_price = (exchange_amount * exchange_rate).quantize(cents, ROUND_HALF_UP)

    return exchange_amount, exchange_rate, exchange_price
