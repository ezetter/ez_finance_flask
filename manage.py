import os

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.models import db, Account, Investment, AccountHistory
from webapp.session_helper import PickleSessionInterface

# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Account=Account,
        Investment=Investment,
        AccountHistory=AccountHistory
    )

path = 'tmp/app_session'
if not os.path.exists(path):
    os.makedirs(path, exist_ok=True)
    os.chmod(path, int('700', 8))

app.session_interface = PickleSessionInterface(path)

if __name__ == "__main__":
    manager.run()
