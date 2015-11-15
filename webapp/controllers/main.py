from flask import Blueprint, redirect, url_for, render_template
from webapp.models import db, Account, Investment
from webapp.forms import AccountForm, InvestmentForm

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates'
)


@main_blueprint.route("/", methods=['GET', 'POST'])
def index():
    accounts = Account.query.all()
    form = AccountForm()
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        form.name.data = ''
        act = Account(name=name, category=category)
        db.session.add(act)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("index.html", accounts=accounts, form=form)


@main_blueprint.route("/edit/<int:account_id>", methods=['GET', 'POST'])
def edit(account_id):
    account = Account.query.get(account_id)
    form = AccountForm(obj=account)
    if form.validate_on_submit():
        account.name = form.name.data
        account.category = form.category.data
        form.name.data = ''
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("edit.html", account=account, form=form)


@main_blueprint.route("/investment/<int:account_id>", methods=['POST'])
def add_investment(account_id):
    form = InvestmentForm()
    account = Account.query.get(account_id)
    if form.validate_on_submit():
        inv = Investment(name=form.name, symbol=form.symbol, shares=form.shares, account=account)
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("investment.html", account=account, form=form)
