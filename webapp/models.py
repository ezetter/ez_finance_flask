from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import locale

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    owner = db.Column(db.String(64))
    investments = db.relationship('Investment', backref='account')

    def value(self):
        val = sum(inv.shares * inv.price for inv in self.investments
                   if inv.shares and inv.price)
        return locale.currency(val, grouping=True)

    def __repr__(self):
        return '<Account: %r, %r>' % (self.name, self.category)


class Investment(db.Model):
    __tablename__ = 'investments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    symbol = db.Column(db.String(64))
    shares = db.Column(db.Float)
    price = db.Column(db.Float)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    UniqueConstraint('symbol', 'account_id')

    def value(self):
        if self.shares and self.price:
            return locale.currency(self.shares * self.price, grouping=True)

    def formatted_price(self):
        return "{:.2f}".format(self.price)

    def __repr__(self):
        return '<Investment: %r>' % self.name

