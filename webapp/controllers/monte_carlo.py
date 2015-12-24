from flask import Blueprint, render_template
from webapp.lib.stock_util import gen_monte_carlo_paths, stats_from_paths
from webapp.lib.queries import all_accounts_sum
import uuid
import pickle

monte_carlo_blueprint = Blueprint(
    'monte_carlo',
    __name__,
    template_folder='../templates'
)


@monte_carlo_blueprint.route("/monte-carlo")
def monte_carlo():
    start_price = all_accounts_sum()

    paths = gen_monte_carlo_paths(start_price)
    fn = "tmp/{}".format(str(uuid.uuid4()))
    with open(fn, 'wb') as f:
        pickle.dump(paths, f, protocol=4)
    stats = stats_from_paths(paths)
    return render_template("monte_carlo.html", paths=paths, stats=stats, fn=fn)
