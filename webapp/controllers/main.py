from flask import Blueprint, redirect, url_for, render_template, request
from webapp.models import db, Account, Investment
from webapp.forms import AccountForm, InvestmentForm
from webapp.lib.stock_util import update_account_prices, get_current_price
from webapp.lib.queries import account_by_type_sums, all_accounts_sum, account_by_owner_sums, \
    format_sums, daily_historical_sum, retirement_class_sums
import locale

locale.setlocale(locale.LC_ALL, '')

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates'
)


@main_blueprint.route("/", methods=['GET'])
def index():
    accounts = Account.query.all()
    if request.args.get('current'):
        update_account_prices(accounts, db)
    return render_template("index.html", accounts=accounts, total=all_accounts_sum(),
                           account_type_sums=format_sums(account_by_type_sums()),
                           account_owner_sums=format_sums(account_by_owner_sums()),
                           retirement_class_sums=format_sums(retirement_class_sums())
                           )


@main_blueprint.route("/edit/<int:account_id>", methods=['GET', 'POST'])
def edit(account_id):
    account = Account.query.get(account_id)
    form = AccountForm(obj=account)
    form.validate_on_submit()
    print(form.retirement.errors)
    if form.validate_on_submit():
        account.name = form.name.data
        account.category = form.category.data
        account.owner = form.owner.data
        account.retirement = form.retirement.data
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
        owner = form.owner.data
        form.name.data = ''
        retirement = form.retirement.data
        act = Account(name=name, category=category, owner=owner, retirement=retirement)
        db.session.add(act)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("add_account.html", form=form)


@main_blueprint.route("/add-investment/<int:account_id>", methods=['GET', 'POST'])
def add_investment(account_id):
    form = InvestmentForm()
    account = Account.query.get(account_id)
    if form.validate_on_submit():
        if not form.price.data and form.symbol.data:
            form.price.data = get_current_price(form.symbol.data)
        inv = Investment(name=form.name.data, symbol=form.symbol.data,
                         shares=form.shares.data, price=form.price.data,
                         account=account)
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("add_investment.html", account=account, form=form)


@main_blueprint.route("/edit-investment/<int:investment_id>", methods=['GET', 'POST'])
def edit_investment(investment_id):
    investment = Investment.query.get(investment_id)
    form = InvestmentForm(obj=investment)
    if not form.price.data and form.symbol.data:
        form.price.data = get_current_price(form.symbol.data)
    if form.validate_on_submit():
        investment.name = form.name.data
        investment.symbol = form.symbol.data
        investment.shares = form.shares.data
        investment.price = form.price.data
        db.session.add(investment)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template("edit_investment.html", investment=investment, form=form)


@main_blueprint.route("/history", methods=['GET'])
def view_history():
    return render_template("history.html", history=format_sums(daily_historical_sum()))