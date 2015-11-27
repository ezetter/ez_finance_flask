from ..models import Investment, Account
import locale


def account_type_sums(db):
    totals = db.session.query(
        db.func.sum(Investment.price*Investment.shares), Account.category
    ).join(Account.investments).group_by(Account.category).all()
    return [(locale.currency(tot[0], grouping=True), tot[1]) for tot in totals]


def all_accounts_sum(db):
    total = db.session.query(
        db.func.sum(Investment.price*Investment.shares)
    ).join(Account.investments).all()[0][0]
    return locale.currency(total, grouping=True)