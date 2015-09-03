# -*- coding: utf-8 -*-
"""
    api.py
    ~~~~~~

    RESTful API specification and response handle.

    :copyright: (c) 2015 |contributors|.
    :license: BSD, see LICENSE for more details.
"""
from flask import render_template, Blueprint, session, jsonify, request, Response, session, make_response, abort
from config import *
from error import UsageError
from collections import Counter
from scoring import controversy
from content import article_search, twitter_search
import stats
import datetime, time
import json
import db, redis


QUERY_PARAM = 'q'
api = Blueprint('/api', __name__)
sr = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


@api.errorhandler(UsageError)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@api.errorhandler(404)
def handle_404(error):
    return justmime('not-found', status=404)

def loggedin():
    return session.get('username') is not None


@api.before_request
def restrict():
    if not loggedin():
        raise UsageError('not logged in')
    if QUERY_PARAM not in request.args and request.url_rule == '/api/':
        raise UsageError('missing-keyword')


def justmime(r, status=200):
    return Response(r, mimetype="application/json", status=status)


def success(r):
    #: not used by main api
    return jsonify({
        'error' : 0,
        'result' : r
    })


def mysql_date():
    return '%Y-%m-%d'


def make_date(t=None):
    """datetime or None -> sql-ready date-string."""
    f = mysql_date()
    return time.strftime(f) if t is None else time.strftime(f, t)


@api.route('/')
def query():
    q = request.args[QUERY_PARAM]
    u = session['username']
    if db.unique_user_query(q, u):
        db.append_history(q, make_date(), u)
    else:
        db.update_history(q, make_date(), u)
    return justmime(sr.get(q)) if sr.exists(q) else new_query(q)


def new_query(keyword):
    arts = article_search(keyword)
    if len(arts) == 0:
        raise UsageError('no-articles', status_code=200)

    ranked = controversy({
        'tweets' : twitter_search(keyword),
        'articles' : arts,
    })
    ranked_dump = json.dumps(ranked)
    sr.set(keyword, ranked_dump)
    #: expire cache in 60 * 60 * 24 = 86400 seconds
    sr.expire(keyword, 86400)
    keyword_score = sum(a['entropy_sentiment_score'] for a in ranked['result'])
    print(make_date())
    db.append_queries(keyword, keyword_score, make_date())
    return justmime(ranked_dump)


@api.route('/user-history')
def history():
    return success({
        'queries' : db.user_history(session['username'])
    })


@api.route('/trend')
def trending():
    hist = map(lambda x : x['Term'], db.histories())
    if not hist:
            return jsonify({
                "trending" : None,
                "top-5": None
            })
    freq = Counter(hist)
    s = reduce(lambda x,y : x + y, freq.values())
    for k, v in freq.iteritems():
        freq[k] = (float(v) / s) * 100
    return success({
        "trending" : freq,
        "top-5" : sorted(freq, key=freq.get, reverse=True)[:5]
    })


@api.route('/trend/<k>')
def keyword_trend(k):
    return success(db.keyword_trend(k))


@api.route('/trend/<k>.png')
def keyword_trend_png(k):
    """Return a PNG from stats in request
    """
    db_resp = db.keyword_trend(k)
    if len(db_resp) < 2:
        #: not enough data for a plot
        abort(404)
    x = map(lambda x: datetime.datetime.strptime(x['Performed'], '%Y-%m-%d'), db_resp)
    y = map(lambda x: x['EntropyScore'], db_resp)
    stats.keyword_trend(k, x, y)
    response = make_response(stats.keyword_trend(k, x, y).getvalue())
    response.mimetype = 'image/png'
    return response
