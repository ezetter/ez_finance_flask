import pandas.io.data as web
from webapp.models import AccountHistory
from datetime import date, timedelta
from sqlalchemy import and_


def update_account_prices(accounts, db):
    for account in accounts:
        account_total_val = 0
        for investment in account.investments:
            price = get_current_price(investment.symbol)
            account_total_val += price
            investment.price = round(price, 2)
            db.session.add(investment)
            db.session.commit()
        history = AccountHistory.query.filter(
            and_(AccountHistory.account_id == account.id, AccountHistory.snapshot_date == date.today())).all()
        if not history:
            history = AccountHistory()
            history.account = account
            history.snapshot_date = date.today()
        else:
            history = history[0]
        history.value = account_total_val
        db.session.add(history)
        db.session.commit()


def get_current_price(ticker):
    end = date.today()
    start = end - timedelta(days=7)
    return round(get_stock_data(ticker, start, end).ix[-1]['Close'], 3)


def get_stock_data(ticker, start, end):
    return web.DataReader(ticker, 'yahoo', start, end)
