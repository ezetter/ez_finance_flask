from ..models import Investment, Account, AccountHistory, db
import locale


def format_sums(totals):
    all_total = sum(tot[0] for tot in totals)
    return [(locale.currency(tot[0], grouping=True), tot[1], round(tot[0] * 100 / all_total, 1)) for tot in totals]


def account_by_type_sums():
    totals = db.session.query(
        db.func.sum(Investment.price * Investment.shares), Account.category
    ).join(Account.investments).group_by(Account.category).all()
    return totals


def account_by_owner_sums():
    totals = db.session.query(
        db.func.sum(Investment.price * Investment.shares), Account.owner
    ).join(Account.investments).group_by(Account.owner).all()
    return totals


def all_accounts_sum():
    total = db.session.query(
        db.func.sum(Investment.price * Investment.shares)
    ).join(Account.investments).all()[0][0]
    return locale.currency(total, grouping=True)


def daily_historical_sum():
    return db.session.query(
        db.func.sum(AccountHistory.value), AccountHistory.snapshot_date
    ).group_by(AccountHistory.snapshot_date) \
        .order_by(AccountHistory.snapshot_date.desc()).all()
