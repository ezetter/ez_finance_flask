import unittest
from webapp import create_app
from webapp.models import db


class TestUrls(unittest.TestCase):
    def setUp(self):
        app = create_app('webapp.config.TestConfig')
        self.client = app.test_client()

        # Bug workaround
        db.app = app

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_root_ok(self):
        """ Tests if the root URL gives a 200 """

        result = self.client.get('/')
        assert result.status_code == 200


    def test_history_ok(self):
        """ Tests if the history URL gives a 200 """

        result = self.client.get('/history')
        assert result.status_code == 200


    def test_add_account(self):
        """ Tests if the add_account URL gives a 200 """

        result = self.client.get('/add_account')
        assert result.status_code == 200

if __name__ == '__main__':
    unittest.main()
