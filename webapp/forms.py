from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional


class AccountForm(Form):
    name = StringField('Account Name ', validators=[DataRequired()])
    category = StringField('Account Category ')
    retirement = SelectField('Retirement?', choices=[(1,'Yes'),(0,'No')], coerce=int)
    owner = StringField('Account Owner ')
    submit = SubmitField('Submit')


class InvestmentForm(Form):
    name = StringField('Investment Name ', validators=[DataRequired()])
    symbol = StringField('Symbol ')
    shares = DecimalField('Number of Shares', places=3)
    price = DecimalField('Price per Share', places=3, validators=[Optional()])


class MonteCarloForm(Form):
    rate = DecimalField('Rate', places=2)
    sigma = DecimalField('Sigma', places=2)
    time = IntegerField('Years')
    start_val = DecimalField('Initial Value', places=2)
