import pandas.io.data as web
import numpy as np
from webapp.models import AccountHistory
from datetime import date, timedelta
from sqlalchemy import and_
import scipy.stats as scs
import locale


def update_account_prices(accounts, db):
    for account in accounts:
        account_total_val = 0
        for investment in account.investments:
            price = get_current_price(investment.symbol)
            account_total_val += price * investment.shares
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


def gen_monte_carlo_paths(S0, r=0.07, sigma=0.2, T=10, M=120, I=250000):
    ''' Generates Monte Carlo paths for geometric Brownian motion.

    Parameters
    ==========
    S0 : float
        initial stock/index value
    r : float
        constant short rate
    sigma : float
        constant volatility
    T : float
        final time horizon
    M : int
        number of time steps/intervals
    I : int
        number of paths to be simulated

    Returns
    =======
    paths : ndarray, shape (M + 1, I)
        simulated paths given the parameters
    '''
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal(I)
        rand = (rand - rand.mean()) / rand.std()
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt +
                                         sigma * np.sqrt(dt) * rand)
    return paths


def stats_from_paths(paths):
    final_prices = paths[-1]
    stats = {'percentiles': ((1, locale.currency(np.percentile(final_prices, 1), grouping=True)),
                             (5, locale.currency(np.percentile(final_prices, 5), grouping=True)),
                             (10, locale.currency(np.percentile(final_prices, 10), grouping=True)),
                             (25, locale.currency(np.percentile(final_prices, 25), grouping=True)),
                             (50, locale.currency(np.percentile(final_prices, 50), grouping=True)),
                             (75, locale.currency(np.percentile(final_prices, 75), grouping=True)),
                             (90, locale.currency(np.percentile(final_prices, 90), grouping=True))),
             'stats': scs.describe(final_prices)}
    return stats
