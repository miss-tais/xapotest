import requests

from decimal import Decimal, ROUND_HALF_UP

from flask import jsonify
from flask_restful import Resource, reqparse

from . import app
from .validators import greater_then_zero_validator, currency_validator
from .models import ExchangeOperation
from .utils import calculate_price


class ExchangeCurrency(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', type=greater_then_zero_validator, location='form', required=True)
    parser.add_argument('currency', type=currency_validator, location='form', required=True)

    def post(self):
        """
        Currency exchange api endpoint.
        Accepts a "currency" (ISO3 code, for example EUR, USD, BTC etc) and "amount".
        Calculates final amount using latest forex prices from OpenExchangeRates API.
        Calculated amount is stored in database as ExchangedOperation record.

        :param amount: Amount (int) - number of last operations. Required parameter.
        :param currency: Currency ISO3 code. Required parameter.

        :return: Serialized ExchangedOperation record
        """
        args = self.parser.parse_args()
        exchange_currency = args.get('currency', "")
        exchange_amount = args.get('amount', 1)

        params = {
            'app_id': app.config['OER_API_KEY'],
            'base': app.config['OER_BASE'],
            'symbols': exchange_currency
        }

        try:
            resp = requests.get('https://openexchangerates.org/api/latest.json', params=params)
            resp.raise_for_status()
        except Exception as e:
            response = jsonify({"message": str(e)})
            response.status_code = 400
            return response

        rates = resp.json()['rates']
        if exchange_currency not in rates:
            response = jsonify({"message": "Exchange rate not found"})
            response.status_code = 400
            return response

        exchange_amount, exchange_rate, exchange_price = calculate_price(exchange_amount, rates[exchange_currency], 8)

        exchange_operation = ExchangeOperation(currency=exchange_currency,
                                               amount=exchange_amount,
                                               price=exchange_price,
                                               rate=exchange_rate)
        exchange_operation.save()

        response = jsonify(exchange_operation.serialize())
        response.status_code = 201

        return response


class LatsExchangeOperations(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('currency', type=currency_validator, location='args')
    parser.add_argument('number', type=greater_then_zero_validator, location='args')

    def get(self):
        """
        Latest currency exchange operations api endpoint.

        :param number: Number (int) - number of last operations. Default: 1. Optional parameter.
        :param currency: Currency ISO3 code. Default: "". Optional parameter.

        :return: List of serialized ExchangedOperation records
        """
        args = self.parser.parse_args()

        exchange_currency = args.get('currency', "")

        records_number = args.get('number', None)
        records_number = records_number if records_number else 1

        queryset = ExchangeOperation.query

        if exchange_currency:
            queryset = queryset.filter_by(currency=exchange_currency)

        queryset = queryset.order_by(ExchangeOperation.created_at.desc()).limit(records_number).all()

        response = jsonify([i.serialize() for i in queryset])
        response.status_code = 200

        return response
