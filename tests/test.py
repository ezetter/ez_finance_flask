import unittest
from webapp import create_app
from webapp.models import db


class TestIt(unittest.TestCase):
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
        """ Tests if the root URL gives a 100 """

        result = self.client.get('/')
        assert result.status_code == 200


if __name__ == '__main__':
    unittest.main()
