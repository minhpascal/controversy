# -*- coding: utf-8 -*-
"""
    api.py
    ~~~~~~

    RESTful API specification and response handle.

    :copyright: (c) 2015 |contributors|.
    :license: BSD, see LICENSE for more details.
"""
from flask import render_template, Blueprint, session, jsonify, request, Response, session
from config import *
from error import UsageError
from collections import Counter
from scoring import controversy
from content import article_search, twitter_search
import datetime, time
import json
import db, redis


QUERY_PARAM = 'q'
HISTORY_ENDPOINT = 'user-history'
STREAM_ENDPOINT = 'stream'


api = Blueprint('/api', __name__)
sr = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


@api.errorhandler(UsageError)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def loggedin():
    return session.get('username') is not None


@api.before_request
def restrict():
    if not loggedin():
        raise UsageError('not logged in')
    if QUERY_PARAM not in request.args and request.path.split('/')[-1] not in [HISTORY_ENDPOINT, STREAM_ENDPOINT]:
        raise UsageError('missing keyword')


def justmime(r):
    return Response(r, mimetype="application/json", status=200)


def success(r):
    #: not used by main api
    r.update({'error':0})
    return jsonify(r)


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

    cached = sr.get(q)
    return justmime(cached) if cached else new_query(q)


def new_query(keyword):
    arts = article_search(keyword)
    if len(arts) == 0:
        raise UsageError('no-articles', status_code=200)

    ranked = json.dumps(controversy({
        'tweets' : twitter_search(keyword),
        'articles' : arts,
        'error' : 0
    }))

    sr.set(keyword, ranked)
    return justmime(ranked)


@api.route('/%s' % HISTORY_ENDPOINT)
def history():
    return success({
        'queries' : db.user_history(session['username'])
    })


@api.route('/%s' % STREAM_ENDPOINT)
def trending():
    hist = map(lambda x : x['Term'], db.histories())
    freq = Counter(hist)
    s = reduce(lambda x,y : x + y, freq.values())
    for k, v in freq.iteritems():
        freq[k] = (float(v) / s) * 100
    return success({
        "trending" : freq,
        "top-5" : sorted(freq, key = freq.get, reverse = True)[:5]
    })


@api.route('/distributions')
def distributions():
    pass
