from flask import Blueprint
from flask_restful import Api

from .views import ExchangeCurrency, LatsExchangeOperations


api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)

api.add_resource(ExchangeCurrency, '/grab_and_save')
api.add_resource(LatsExchangeOperations, '/last')
