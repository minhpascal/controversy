#-*- coding: utf-8 -*-
"""
    stats.py
    ~~~~~~~~

    graphs with matplotlib.
"""
from StringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

def normalize(x):
    """normalizes axis (a list of numbers)
    """
    inf = min(x)
    sup = max(x)
    diff = sup - inf
    return map(lambda x_i: (x_i - inf) / (diff), x)


def keyword_trend(keyword, x, y):
    """plot x vs y
    """
    fig = Figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_title('"%s" controversy vs. time' % keyword)
    ax.set_ylabel('controversy entropy-based score')
    ax.set_xlabel('time')
    ax.plot_date(x, y, fmt='bo-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.grid(True)

    fig.autofmt_xdate()
    fig.tight_layout()
    canvas = FigureCanvasAgg(fig)
    png = StringIO()
    canvas.print_png(png)
    return png
