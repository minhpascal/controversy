# -*- coding: utf-8 -*-
"""
    api.py
    ~~~~~~~

    RESTful API
    Twitter and article scraper, controversy call, and response.

    :copyright: (c) 2015 Ismini Lourentzou, Graham Dyer, Lisa Huang.
    :license: BSD, see LICENSE for more details.
    :author: Graham Dyer
"""
from flask import render_template, Blueprint, session, jsonify, request, Response
from config import *
from error import UsageError
from twython import Twython 
from collections import Counter
from bs4 import BeautifulSoup
from scoring import controversy
import urllib, urllib2, cookielib, datetime, time, json, db, re, random, requests
api = Blueprint('/api', __name__)
from app import loggedin



QUERY_PARAM = 'q'
MAX_ATTEMPTS = 10
MAX_TWEETS = 1000
MAX_ARTICLES = 100
HISTORY_ENDPOINT = 'user-history'
STREAM_ENDPOINT = 'stream'


@api.errorhandler(UsageError)
def handle_error(error):
    response = jsonify(error.todict())
    response.status_code = error.status_code
    return response

@api.before_request
def restrict():
    if not loggedin():
        raise UsageError('not logged in')
    if QUERY_PARAM not in request.args and request.path.split('/')[-1] not in [HISTORY_ENDPOINT, STREAM_ENDPOINT]:
        raise UsageError('missing keyword')


def success(r):
    r.update({'error':0})
    return jsonify(r)

def make_date(t=None):
    """datetime or None -> sql-ready date-string."""

    f = '%Y-%m-%d'
    return time.strftime(f) if t is None else time.strftime(f, t)



@api.route('/')
def query():
    q = request.args[QUERY_PARAM]
    u = session['username']
    if db.unique_user_query(q, u):
        db.append_history(q, make_date(), u)

    return new_query(q)

def new_query(keyword):
    #: return unranked until ported method is available 
    #db.add_query(keyword, make_date())
    arts = nyt_search(keyword)
    if len(arts) == 0:
        raise UsageError('no-articles', status_code=200)
    return success(controversy({
            'tweets' : tw_search(keyword),
            'articles' : arts
    }))

def format_date(s):
    return s.strftime('%Y%m%d')

def nyt_search(keyword):
    """Get articles based on keyword."""
    #: tweets are < 10 days old; articles should match
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=10)

    params = urllib.urlencode({
        'q' : keyword,
        'begin_date' : format_date(last_week),
        'end_date' : format_date(today),
        'api-key' : NYT_KEY,
        'facet_field' : 'source'
    })


    response = urllib2.urlopen("http://api.nytimes.com/svc/search/v2/articlesearch.json?%s" % params)

    return make_nyt_pretty(keyword, json.load(response))


def make_nyt_pretty(keyword, json_response):
    res = []
    for article in json_response['response']['docs']:
        if 'corrections' in article['headline']['main'].lower():
            continue
        has_multimedia = len(article['multimedia']) > 1
        has_byline = article['byline']

        strip = re.compile(r'(<!--.*?-->|<[^>]*>)') 
        ab = strip.sub('', article['abstract'] or article['lead_paragraph'])
        re.sub('[<>]', '', ab)

        url = article['web_url']

        data = {
                'url' : url,
                'author' : article['byline']['original'] if has_byline else None,
                'abstract' : ab,
                'title' : article['headline']['main'],
                'source' : article['source'],
                'published' : make_date(time.strptime(article['pub_date'][:10], '%Y-%m-%d')),
                'xlarge' : 'http://www.nytimes.com/%s' % article['multimedia'][1]['url'] if has_multimedia else None,
                'full' : get_full(url)
        }

        res.append(data)
    return res

def get_full(url):
    """nyt url --> full article text."""
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(urllib2.Request(url))
    soup = BeautifulSoup(response.read())
    body = soup.findAll('p', {'class' : ['story-body-text', 'story-content']})

    res = " ".join(p.text for p in body) 
    if not res:
        raise UsageError('failed-to-parse')
    jar.clear()
    return res

def tw_search(keyword):
    twitter = get_auth()
    tweets = []
    for i in xrange(MAX_ATTEMPTS):
        if MAX_TWEETS < len(tweets):
            break

        res = twitter.search(q=keyword, count=100, lang="en") if i == 0 else twitter.search(q=keyword, include_entities='true', max_id=next_max)

        for r in res['statuses']:
            dirty = r['text']
            clean = clean_tweet(dirty)
            tweets.append({
                'tweet' : dirty,
                'clean' : clean, 
                'author' : r['user']['screen_name'],
                'followers' : r['user']['followers_count'],
                'pimg' : r['user']['profile_image_url_https'],
                'sentiment' : get_sentiment(clean)
            })
        try:
            next_res = results['search_metadata']['next_results']
            next_max = next_res.split('max_id=')[1].split('&')[0]
        except:
            break
    return tweets

def get_auth():
    auth = Twython(API_KEY, API_SECRET, oauth_version = 2)
    return Twython(API_KEY, access_token = auth.obtain_access_token())

def clean_tweet(dirty):
    return ' '.join(re.sub(r"(?:\@|https?\://)\S+", "", dirty.strip('#')).split())

def get_sentiment(tweet):
    """Get sentiment of a ( clean ) tweet."""

    if 'test' in request.args:
        return random.choice([0,2,4])

    params = urllib.urlencode({
        "api-key" : SENTIGEM_KEY,
        "text" : tweet
    })
    response = urllib2.urlopen("https://api.sentigem.com/external/get-sentiment?%s" % params)
    res = json.load(response)
    print('sentiment cost ==> %s' % res['cost'])
    if res['cost'] != '0.000000':
        raise UsageError('sentigem is charging us')

    return {'negative':0, 'neutral':2, 'positive':4}[res['polarity']]




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
        "trending" : freq
    })
