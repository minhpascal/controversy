# -*- coding: utf-8 -*-
from config import REDIS_HOST, REDIS_PORT
from scoring import controversy
from content import article_search, twitter_search, article_comments
import db
import redis
import json
import datetime

sr = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

def perform(keyword):
    """Provide ``keyword`` for content retrieval, scoring.
    """
    articles = article_search(keyword)
    if len(articles) == 0:
        raise UsageError('no-articles', status_code=200)

    return {
        'result': controversy(articles, twitter_search(keyword)),
        'ts': datetime.datetime.utcnow(),
        'keyword': keyword,
        'ok': 1
    }


def new_query(keyword):
    """Provide ``keyword`` for content retrieval,
    scoring, cache, and history entry.
    """
    ranked = perform(keyword)
    ranked['ts'] = ranked['ts'].isoformat()
    ranked_dump = json.dumps(ranked)
    sr.set(keyword, ranked_dump)
    # expire cache in 60 * 60 * 24 = 86400 seconds (24 hours)
    sr.expire(keyword, 86400)
    keyword_score = sum(a['score'] for a in ranked['result'])
    db.append_queries(keyword, keyword_score)
    return ranked_dump
