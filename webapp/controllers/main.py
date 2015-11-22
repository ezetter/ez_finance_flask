from flask import Blueprint, redirect, url_for, render_template, request
from webapp.models import db, Account, Investment
from webapp.forms import AccountForm, InvestmentForm
from webapp.lib.stock_util import update_account_prices

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates'
)


@main_blueprint.route("/", methods=['GET'])
def index():
    accounts = Account.query.all()
    if request.args.get('current'):
        update_account_prices(accounts)
    total = round(sum(inv.price * inv.shares for account in accounts
                      for inv in account.investments if inv.price), 2)
    return render_template("index.html", accounts=accounts, total=total)


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


@main_blueprint.route("/add_account", methods=['GET', 'POST'])
def add_account():
    form = AccountForm()
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        form.name.data = ''
        act = Account(name=name, category=category)
        db.session.add(act)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("add_account.html", form=form)


@main_blueprint.route("/add-investment/<int:account_id>", methods=['GET', 'POST'])
def add_investment(account_id):
    form = InvestmentForm()
    account = Account.query.get(account_id)
    if form.validate_on_submit():
        inv = Investment(name=form.name.data, symbol=form.symbol.data,
                         shares=form.shares.data, price = form.price.data,
                         account=account)
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("add_investment.html", account=account, form=form)


@main_blueprint.route("/edit-investment/<int:investment_id>", methods=['GET', 'POST'])
def edit_investment(investment_id):
    inv = Investment.query.get(investment_id)
    form = InvestmentForm(obj=inv)
    print(inv)
    if form.validate_on_submit():
        inv.name = form.name.data
        inv.symbol = form.symbol.data
        inv.shares = form.shares.data
        inv.price = form.price.data
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("edit_investment.html", investment=inv, form=form)
