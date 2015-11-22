import pandas.io.data as web
import datetime


def get_current_price(ticker):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=7)
    return get_stock_data(ticker, start, end).ix[-1]


def get_stock_data(ticker, start, end):
    return web.DataReader(ticker, 'yahoo', start, end)