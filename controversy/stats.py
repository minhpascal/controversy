#-*- coding: utf-8 -*-
"""
    stats.py
    ~~~~~~~~
    Visualizations with matplotlib.
"""

from StringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


def keyword_trend(keyword, x, y):
    """plot x vs y
    """
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_title('"%s" controversy vs. time' % keyword)
    ax.set_ylabel('controversy entropy-based score')
    ax.set_xlabel('time')
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvasAgg(fig)
    png = StringIO()
    canvas.print_png(png)
    return png
