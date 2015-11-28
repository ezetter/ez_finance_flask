from flask import Blueprint, render_template
from webapp.lib.queries import account_by_type_sums, account_by_owner_sums
from webapp.models import db
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import make_response
import io


chart_blueprint = Blueprint(
    'chart',
    __name__,
    template_folder='../templates'
)


@chart_blueprint.route("/bars.png")
def category_bar_charts():
    sns.set(style="whitegrid")
    sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
    f, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=False)
    account_type_sums = sorted(account_by_type_sums(db), reverse=True)
    x = [a[1] for a in account_type_sums]
    y = [a[0] for a in account_type_sums]
    sns.barplot(x, y, palette="BuGn_d", ax=ax1)
    ax1.set_ylabel("By Category")

    account_owner_sums = sorted(account_by_owner_sums(db), reverse=True)
    x = [a[1] for a in account_owner_sums]
    y = [a[0] for a in account_owner_sums]
    sns.barplot(x, y, palette="Blues_d", ax=ax2)
    ax2.set_ylabel("By Owner")
    sns.despine(left=True)
    f.tight_layout()
    canvas = FigureCanvas(plt.gcf())
    png_output = io.BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@chart_blueprint.route("/charts")
def charts():
    return render_template("charts.html")
