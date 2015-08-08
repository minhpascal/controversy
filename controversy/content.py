# -*- coding: utf-8 -*-
"""
    content.py
    ~~~~~~~~~~~
    Interfaces with api endpoints (as defined in api.py).
"""
from bs4 import BeautifulSoup
from config import *
from twython import Twython
import re, json
import time, datetime
import urllib, urllib2, cookielib
from sentiment import analyse, is_positive, is_negative
from functools import partial
from operator import is_not
from flask import current_app


MAX_ATTEMPTS = 7
MAX_COMMENTARY = 500


class Tweet(object):
    """A tweet
       holds basic attributes and finds sentiment
    """

    def __init__(self, j):
        self.tweet = j['text']
        self.clean_tweet = self._clean()
        self.author = j['user']['screen_name']
        self.followers = j['user']['followers_count']
        self.pimg = j['user']['profile_image_url']
        self.identifier = j['id']
        self.sentiment = self._sentiment()
        self.is_negative = is_negative(self.sentiment)
        self.is_positive = is_positive(self.sentiment)

    def to_dict(self):
        return self.__dict__

    def _clean(self):
        return ' '.join(re.sub(r"(?:\@|https?\://)\S+", "", self.tweet.strip('#')).split())

    def _sentiment(self):
        #if current_app.debug:
        #    import random
        #    return random.choice([0,2,4])
        return analyse(self.clean_tweet)



class Article(object):
    """A NYT article
       holds basic attibutes and gets full text 
    """ 

    def __init__(self, j):
        self.lead = j['lead_paragraph']
        self.abstract = j['abstract']
        self.title = j['headline']['main']
        self.source = j['source']
        self.byline = j['byline']['original'] if (j['byline']) else None
        self.abstract = self._no_html_ab()
        self.url = j['web_url']
        self.xlarge = 'http://www.nytimes.com/%s' % j['multimedia'][1]['url'] if len(j['multimedia']) > 1 else None
        self.published = j['pub_date'][:10]
        self.full = self._full_text()

    def to_dict(self):
        return self.__dict__ if (self.full is not None and len(self.full)) != 0 else None

    def _no_html_ab(self):
        return BeautifulSoup(self.abstract or self.lead, 'html.parser').getText()

    def _full_text(self):
        """nyt url --> full article text."""
        if 'Paid Notice:' in self.title or 'video/multimedia' in self.url:
            return None
        jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        response = opener.open(urllib2.Request(self.url))
        soup = BeautifulSoup(response.read(), 'lxml')
        body = soup.findAll('p', {'class' : ['story-body-text', 'story-content']})
        res = " ".join(p.text for p in body) 
        jar.clear()
        return res

    def _comments(self):
        params = urllib.urlencode({
            'api-key' : NYT_COMMUNITY_KEY,
            'url' : self.url
        })
        response = urllib2.urlopen("http://api.nytimes.com/svc/community/v3/user-content/url.json?%s" % params)
        #print(json.loads(response.read()))


def nyt_query_date(s):
    return s.strftime('%Y%m%d')


def article_search(keyword):
    """Get articles based on keyword."""
    #: tweets are < 10 days old; articles should match
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=11)

    params = urllib.urlencode({
        'q' : keyword,
        'begin_date' : nyt_query_date(last_week),
        'end_date' : nyt_query_date(today),
        'api-key' : NYT_KEY,
        'facet_field' : 'source'
    })

    response = urllib2.urlopen("http://api.nytimes.com/svc/search/v2/articlesearch.json?%s" % params)
    return filter(partial(is_not, None), map(lambda x: Article(x).to_dict(), json.loads(response.read())['response']['docs']))


def twitter_search(keyword):
    twitter = get_auth()
    tweets = []

    for i in xrange(MAX_ATTEMPTS):
        if MAX_COMMENTARY < len(tweets):
            break

        response = twitter.search(q=keyword, count=100, lang="en") if i == 0 else twitter.search(q=keyword, include_entities='true', max_id=next_max)
        tweets += map(lambda x: Tweet(x).to_dict(), response['statuses'])
        try:
            next_res = results['search_metadata']['next_results']
            next_max = next_res.split('max_id=')[1].split('&')[0]
        except:
            break
    return tweets


def get_auth():
    auth = Twython(API_KEY, API_SECRET, oauth_version=2)
    return Twython(API_KEY, access_token = auth.obtain_access_token())
