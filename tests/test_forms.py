from webapp import create_app
from webapp.models import db, Account
from flask import url_for
from flask.ext.testing import TestCase


class TestForms(TestCase):
    def create_app(self):
        app = create_app('webapp.config.TestConfig')
        self.client = app.test_client()

        app.config['WTF_CSRF_ENABLED'] = False

        # Bug workaround
        db.app = app

        db.create_all()

        return app

    # def setUp(self):


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_account(self):
        result = self.client.post('/add_account', data=dict(
            name="Bob's Funds Inc.",
            retirement=1,
            category='401k',
            owner='Joe'
        ))
        self.assert_redirects(result, url_for('.index'))
        account = Account.query.first()
        self.assertEqual(account.name, "Bob's Funds Inc.")

    def test_add_account_failed_validation(self):
        self.client.post('/add_account', data=dict(
            retirement=1,
            category='401k',
            owner='Joe'
        ))
        self.assert_template_used('add_account.html')
