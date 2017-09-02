import pandas_datareader.data as web
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
    return round(get_stock_data(ticker, start, end)['last'][0], 3)


def get_stock_data(ticker, start, end):
    return web.get_quote_yahoo(ticker)


def gen_monte_carlo_paths(s0, r=0.07, sigma=0.2, time=10, its=250000, annual_contrib=0):
    ''' Generates Monte Carlo paths for geometric Brownian motion.

    Parameters
    ==========
    s0 : float
        initial stock/index value
    r : float
        constant short rate
    sigma : float
        constant volatility
    time : float
        final time horizon
    M : int
        number of time steps/intervals
    its : int
        number of paths to be simulated

    Returns
    =======
    paths : ndarray, shape (M + 1, I)
        simulated paths given the parameters
    '''
    interval = 12
    m = int(time * interval)
    dt = 1.0 / interval
    paths = np.zeros((m + 1, its), np.float64)
    paths[0] = s0
    for t in range(1, m + 1):
        rand = np.random.standard_normal(its)
        rand = (rand - rand.mean()) / rand.std()
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt +
                                         sigma * np.sqrt(dt) * rand) + annual_contrib / interval

    return paths


def stats_from_paths(paths):
    final_prices = paths[-1]
    stats = {'percentiles': ((1, locale.currency(np.percentile(final_prices, 1), grouping=True)),
                             (5, locale.currency(np.percentile(final_prices, 5), grouping=True)),
                             (10, locale.currency(np.percentile(final_prices, 10), grouping=True)),
                             (25, locale.currency(np.percentile(final_prices, 25), grouping=True)),
                             (50, locale.currency(np.percentile(final_prices, 50), grouping=True)),
                             (75, locale.currency(np.percentile(final_prices, 75), grouping=True)),
                             (90, locale.currency(np.percentile(final_prices, 90), grouping=True)),
                             (95, locale.currency(np.percentile(final_prices, 95), grouping=True)),
                             (99, locale.currency(np.percentile(final_prices, 99), grouping=True))),
             'stats': scs.describe(final_prices)}
    return stats


def compound(s0, r=0.07, t=10, annual_contrib=0):
    vals = [s0]
    interval = 12
    m = int(t * interval)
    v = s0
    for t in range(1, m + 1):
        v += v * (r / interval) + (annual_contrib / interval)
        vals.append(v)
    return vals