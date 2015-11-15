from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length


class AccountForm(Form):
    name = StringField('Account Name ', validators=[DataRequired()])
    category = StringField('Account Category ')
    submit = SubmitField('Submit')


def AvailableAccounts():
    pass


class InvestmentForm(Form):
    name = StringField('Investment Name ', validators=[DataRequired()])
    symbol = StringField('Symbol ')
    shares = DecimalField('Number of Shares', places=3)
