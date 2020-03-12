from sqlalchemy.sql import func

from . import db


class ExchangeOperation(db.Model):
    """Data model for USD currency exchange."""

    __tablename__ = 'exchange_operation'

    id = db.Column(db.Integer, primary_key=True)

    currency = db.Column(db.String(3), index=True)

    amount = db.Column(db.Integer, index=False)

    rate = db.Column(db.Numeric(20, 8), index=False)

    price = db.Column(db.Numeric(20, 8), index=False)

    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'{self.amount} USD equals {self.price} {self.currency}'

    def save(self):
        """Method to update ExchangeOperation"""
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        """Return object data in serializable format"""

        return {
            'id': self.id,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'currency': self.currency,
            'amount': self.amount,
            'rate': self.rate,
            'price': self.price
        }