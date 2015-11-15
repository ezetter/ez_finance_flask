from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    investments = db.relationship('Investment', backref='account')

    def __repr__(self):
        return '<Account: %r, %r>' % (self.name, self.category)


class Investment(db.Model):
    __tablename__ = 'investment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    symbol = db.Column(db.String(64), unique=True)
    shares = db.Column(db.Float)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __repr__(self):
        return '<Investment: %r>' % self.name

