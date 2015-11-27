# -*- coding: utf-8 -*-
"""
    api.py
    ~~~~~~

    RESTful API specification and response handle.
"""
from flask import render_template, Blueprint, session, jsonify, request, Response, session, make_response, abort
from error import UsageError
from collections import Counter
from querier import new_query, sr
import stats
import datetime
import json
import db 
import redis


QUERY_PARAM = 'q'
api = Blueprint('/api', __name__)


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
    # not used by main api; see ``querier``
    return jsonify({
        'error' : 0,
        'result' : r
    })


@api.route('/')
def query():
    q = request.args[QUERY_PARAM]
    u = session['username']
    if db.unique_user_query(q, u):
        db.append_history(q, u)
    else:
        db.update_history(q, u)
    return justmime(sr.get(q)) if sr.exists(q) else justmime(new_query(q))


@api.route('/user-history')
def history():
    return success({
        'queries' : db.user_history(session['username'])
    })


def get_largest_for_key(source, n):
    """get top ``n`` items from list of dicts ``source``
    where duplicate keys exist but ``source`` is sorted (desc)
    """
    processed_keys = set()
    processed = []
    ap = processed.append
    for i in source:
        if len(processed) > n:
            break
        t = i['Term']
        if t not in processed_keys:
            processed_keys.add(t)
            ap(i)

    return processed


@api.route('/trend')
def trending():
    """Trending keywords in demo
    """
    hist = map(lambda x : x['Term'], db.histories())
    if not hist:
            return jsonify({
                "trending" : None,
                "top-5": None
            })
    freq = Counter(hist)
    s = sum(freq.values())
    for k, v in freq.iteritems():
        freq[k] = (float(v) / s) * 100


    return success({
        "trending" : freq,
        "controversial": get_largest_for_key(db.most_controversial(), 4),
        "top-5" : sorted(freq, key=freq.get, reverse=True)[:5]
    })


@api.route('/trend/<k>')
def keyword_trend(k):
    """JSON for historical score of keyword ``k``
    """
    return success(db.keyword_trend(k))


@api.route('/trend/<k>.png')
def keyword_trend_png(k):
    """PNG from ``stats`` for historical score of keyword ``k``
    """
    db_resp = db.keyword_trend(k)
    if len(db_resp) < 2:
        # not enough data for a plot
        abort(404)
    x = map(lambda x: x['Performed'], db_resp)
    y = map(lambda x: x['EntropyScore'], db_resp)
    if 'nonorm' not in request.args:
        y = stats.normalize(y)
    response = make_response(stats.keyword_trend(k, x, y).getvalue())
    response.mimetype = 'image/png'
    return response
