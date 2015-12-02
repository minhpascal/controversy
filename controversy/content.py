# -*- coding: utf-8 -*-
"""
    content.py
    ~~~~~~~~~~~

    Interfaces with api endpoints (as defined in api.py).

    This module gets, well, content for scoring.
    Namely, it fetches NYTimes articles (metadata & full-text) and tweets based on a keyword.
"""
from bs4 import BeautifulSoup
from config import *
from twython import Twython
import re, json
import time, datetime
import urllib, urllib2, cookielib
from sentiment import textblob, is_positive, is_negative, sentistrength
from functools import partial
from operator import is_not


MAX_ATTEMPTS = 6
MAX_COMMENTARY = 500
TAG_RE = re.compile(r'<[^>]+>')


class SocialContent(object):

    def __init__(self, clean, dirty, sentis=False):
        self.clean = clean
        self.dirty = dirty
        self.sentiment = self._sentiment(sentis)
        self.is_negative = is_negative(self.sentiment)
        self.is_positive = is_positive(self.sentiment)

    def to_dict(self):
        return self.__dict__

    def _sentiment(self, sentis):
        return sentistrength(self.clean) if sentis else textblob(self.clean)


class Tweet(SocialContent):
    """A tweet
       holds basic attributes and finds sentiment
    """

    def __init__(self, j, sentis=False):
        dirty = j['text']
        SocialContent.__init__(self, self._clean(dirty), dirty, sentis=sentis)

        self.ts = j['created_at']
        self.retweets = j['retweet_count']
        self.retweeted = j['retweeted']
        self.location = j['user']['location']
        self.author = j['user']['screen_name']
        self.n_statuses = j['user']['statuses_count']
        self.time_zone = j['user']['time_zone']
        self.followers = j['user']['followers_count']
        self.pimg = j['user']['profile_image_url']
        self.identifier = j['id']


    def _clean(self, dirty):
        return ' '.join(re.sub(r"(?:\@|https?\://)\S+", "", dirty.strip('#')).split())



class Comment(SocialContent):
    """A comment 
       holds basic attributes and finds sentiment
    """

    def __init__(self, j, sentis=False):
        dirty = j['commentBody']
        SocialContent.__init__(self, self._clean(dirty), dirty, sentis)

        self.userLocation = j['userLocation']
        self.n_replies = j['replyCount']
        self.ts = j['updateDate']
        self.n_recommendations = j['recommendations']
        self.abuseFlag = j['reportAbuseFlag']

    def _clean(self, dirty):
        return TAG_RE.sub('', dirty)


class Article(object):
    """A NYT article
       holds basic attibutes and gets full-text 
    """ 

    def __init__(self, j, sentis=False):
        self.lead = j['lead_paragraph']
        self.abstract = j['abstract']
        self.title = j['headline']['main']
        self.source = j['source']
        self.byline = j['byline']['original'] if (j['byline']) else None
        self.abstract = self._no_html_ab()
        self.url = j['web_url']
        self.xlarge = 'https://www.nytimes.com/%s' % j['multimedia'][1]['url'] if len(j['multimedia']) > 1 else None
        self.published = j['pub_date'][:10]
        self.full = self._full_text(sentis)
        self.comments = article_comments(self.url, sentis=sentis)

    def to_dict(self):
        return self.__dict__ if (self.full is not None and len(self.full)) != 0 else None

    def _no_html_ab(self):
        return BeautifulSoup(self.abstract or self.lead, 'html.parser').getText()

    def _full_text(self, sentis):
        """nyt url --> full article text
        """
        if 'Paid Notice:' in self.title or 'video/multimedia' in self.url:
            return None
        jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        response = opener.open(urllib2.Request(self.url))
        soup = BeautifulSoup(response.read(), 'html.parser')
        body = soup.findAll('p', {'class' : ['story-body-text', 'story-content']})
        res = ' '.join(p.text for p in body)
        #res = ''.join(map(lambda x: '<p>%s</p>' % x.text, body)) if sentis else ' '.join(p.text for p in body)
        jar.clear()
        return res


def nyt_query_date(s):
    return s.strftime('%Y%m%d')


def article_search(keyword, sentis=False):
    """Get articles based on keyword."""
    # tweets are < 10 days old; articles should match
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=11)

    params = urllib.urlencode({
        'q': keyword,
        'begin_date': nyt_query_date(last_week),
        'end_date': nyt_query_date(today),
        'api-key': NYT_KEY,
        'facet_field': 'source'
    })

    response = urllib2.urlopen('http://api.nytimes.com/svc/search/v2/articlesearch.json?%s' % params)
    # an Article will be None if it doesn't have body text (thus the partial)
    # return an array of Article objects that have a body text
    return filter(partial(is_not, None), map(lambda x: Article(x, sentis=sentis), json.loads(response.read())['response']['docs']))


def article_comments(url, offset=0, sentis=False):
    comments = []

    for i in xrange(MAX_ATTEMPTS):
        if MAX_COMMENTARY < len(comments):
            break

        params = urllib.urlencode({
            'url': url,
            'api-key': NYT_COMMUNITY_KEY,
            'offset': i * 25
        })

        response = urllib2.urlopen('http://api.nytimes.com/svc/community/v3/user-content/url.json?%s' % params)
        try:
            comment_batch = json.loads(response.read())['results']['comments']
        except ValueError:
            # no json could be decoded
            break

        comments += map(lambda x: Comment(x, sentis=sentis).to_dict(), comment_batch)

    return comments


def twitter_search(keyword, sentis=False):
    twitter = get_auth()
    tweets = []

    for i in xrange(MAX_ATTEMPTS):
        if MAX_COMMENTARY < len(tweets):
            break

        response = twitter.search(q=keyword, count=100, lang='en') if i == 0 else twitter.search(q=keyword, include_entities=True, max_id=next_max)
        tweets += map(lambda x: Tweet(x, sentis=sentis), response['statuses'])
        try:
            next_res = response['search_metadata']['next_results']
            next_max = next_res.split('max_id=')[1].split('&')[0]
        except KeyError:
            break

    return tweets


def get_auth():
    auth = Twython(API_KEY, API_SECRET, oauth_version=2)
    return Twython(API_KEY, access_token = auth.obtain_access_token())
