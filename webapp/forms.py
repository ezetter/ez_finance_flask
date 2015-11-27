from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Optional


class AccountForm(Form):
    name = StringField('Account Name ', validators=[DataRequired()])
    category = StringField('Account Category ')
    owner = StringField('Account Owner ')
    submit = SubmitField('Submit')


class InvestmentForm(Form):
    name = StringField('Investment Name ', validators=[DataRequired()])
    symbol = StringField('Symbol ')
    shares = DecimalField('Number of Shares', places=3)
    price = DecimalField('Price per Share', places=3, validators=[Optional()])
