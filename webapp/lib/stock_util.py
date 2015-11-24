import pandas.io.data as web
import datetime


def update_account_prices(accounts, db):
    for account in accounts:
        for investment in account.investments:
            price = get_current_price(investment.symbol)
            investment.price = round(price, 2)
            db.session.add(investment)
            db.session.commit()


def get_current_price(ticker):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=7)
    return round(get_stock_data(ticker, start, end).ix[-1]['Close'], 3)


def get_stock_data(ticker, start, end):
    return web.DataReader(ticker, 'yahoo', start, end)