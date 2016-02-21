import unittest
from webapp import create_app
from webapp.models import db, Account, Investment
from webapp.lib.queries import all_accounts_sum


class TestLibs(unittest.TestCase):
    def setUp(self):
        app = create_app('webapp.config.TestConfig')
        self.client = app.test_client()

        # Bug workaround
        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def seed_db(self):
        name = 'Some Account'
        category = 'My 401k'
        owner = 'Jane Dow'
        retirement = 1
        act = Account(name=name, category=category, owner=owner, retirement=retirement)
        db.session.add(act)
        inv = Investment(name='SPDR S&P 500 ETF', symbol='SPY',
                         shares=100, price=2020.38,
                         account=act)
        db.session.add(inv)
        inv = Investment(name='iShares Russell 2000', symbol='IWM',
                         shares=50, price=25.05,
                         account=act)
        db.session.add(inv)

        act = Account(name='My Brokerage', category='Brokerage', owner='Bob Dow', retirement=0)
        db.session.add(act)
        inv = Investment(name='VANGUARD TOTAL STOCK MARKET ETF', symbol='VTI',
                         shares=152.63, price=2020.38,
                         account=act)
        db.session.add(inv)

        db.session.commit()

    def test_all_accounts_sum(self):
        self.seed_db()
        total = all_accounts_sum()
        self.assertEqual(total, 2020.38 * 100 + 50 * 25.05 + 152.63 * 2020.38)


if __name__ == '__main__':
    unittest.main()
