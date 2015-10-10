from config import REDIS_HOST, REDIS_PORT
from scoring import controversy
from content import article_search, twitter_search
import db
import redis
import json

sr = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

def new_query(keyword):
    """Provide ``keyword`` for content retrieval,
    scoring, cache, and history entry.
    """
    articles = article_search(keyword)
    if len(articles) == 0:
        raise UsageError('no-articles', status_code=200)

    ranked = controversy(
            articles,
            twitter_search(keyword))
    ranked_dump = json.dumps(ranked)
    sr.set(keyword, ranked_dump)
    # expire cache in 60 * 60 * 24 = 86400 seconds
    sr.expire(keyword, 86400)
    keyword_score = sum(a['entropy_sentiment_score'] for a in ranked['result'])
    db.append_queries(keyword, keyword_score)
    return ranked_dump
