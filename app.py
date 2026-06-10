#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    PIP_PACKAGES_DIR = "./pypackages"
    import sys
    sys.path.insert(0, PIP_PACKAGES_DIR)


from flask import Flask, render_template, request
from flask import Response
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from grades import is_int, data_into_buckets, get_dist_stats

app = Flask(__name__)


def process_post():
    return "<h3>Grades received</h3>\n" + \
        plot_png() + \
        "<p><a href=\"https://faculty.washington.edu/pisan/grade-stats/\">" + \
        "Back to submit more grades</a><p>\n" + \
        "<p><a href=\"/\">" + \
        "Back to submit more grades (/)</a><p>\n"


@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('input-grades.html')
    else:
        return process_post()


def plot_png():
    fig = create_bar_plot()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def create_bar_plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    data = [x for x in request.form['grades'].split('\n') if x.strip() != ""]
    textstr = get_dist_stats(data)
    axis.text(0.02, 0.95, textstr, transform=axis.transAxes, fontsize=10,
              verticalalignment='top', bbox=props)
    xs = ["<50", "50-59", "60-69", "70-79", "80-89", ">=90", "NaN"]
    ys = data_into_buckets(data)
    axis.bar(xs, ys)
    axis.set_xlabel("Decimal Grades")
    axis.set_ylabel("# of Students")
    # fig.suptitle("Course Number")
    return fig



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8088)
