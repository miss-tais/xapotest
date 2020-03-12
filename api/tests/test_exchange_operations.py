import unittest
import json

from flask import Flask

from app import create_app, db
from config import app_config
from app.utils import calculate_price


class ExchangeOperationTestCase(unittest.TestCase):
    """This class represents exchange operations test case"""

    def setUp(self):
        self.app = Flask(__name__, instance_relative_config=False)
        self.app.config.from_object(app_config['test'])

        db.init_app(self.app)

        from app.urls import api_bp
        self.app.register_blueprint(api_bp)

        self.client = self.app.test_client
        self.exchange_operation = {'amount': 10, 'currency': 'USD'}

        # binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_api_grab_and_save(self):
        """Test API can create grab and save exchange operation (POST request)"""

        res = self.client().post('/grab_and_save', data=self.exchange_operation)
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)

        self.assertEqual(data['amount'], self.exchange_operation['amount'])
        self.assertEqual(data['currency'], self.exchange_operation['currency'])
        amount, rate, price = calculate_price(data['amount'], data['rate'], 8)
        self.assertEqual(data['price'], price)

    def test_api_last(self):
        """Test API can retrieve last operations (GET request)."""
        res = self.client().post('/grab_and_save', data=self.exchange_operation)
        self.assertEqual(res.status_code, 201)

        res = self.client().get('/last')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)

        res = self.client().get('/last?currency=RUB')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 0)

        res = self.client().post('/grab_and_save', data=self.exchange_operation)
        self.assertEqual(res.status_code, 201)

        res = self.client().get(f'/last?currency={self.exchange_operation["currency"]}')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 1)

        res = self.client().get(f'/last?currency={self.exchange_operation["currency"]}&number=2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 2)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
