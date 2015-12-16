# -*- coding: utf-8 -*-
"""
    content.py
    ~~~~~~~~~~~

    Interfaces with api endpoints (as defined in api.py).

    This module gets, well, content for scoring.
    Namely, it fetches
        * NYTimes articles (metadata & full-text),
        * comments on NYT articles,
        * and tweets based on a keyword
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
from nltk.corpus import stopwords
from twython.exceptions import TwythonRateLimitError, TwythonError


MAX_ATTEMPTS = 6
MAX_COMMENTARY = 500
TAG_RE = re.compile(r'<[^>]+>')
ARTICLE_SEARCH_BASE = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'
COMMENT_BASE = 'http://api.nytimes.com/svc/community/v3/user-content/url.json?'


class SocialContent(object):
    """Subclasses are wrappers for social APIs
    """
    def __init__(self, clean, dirty, training=False):
        self.clean = clean
        self.dirty = dirty
        if not training:
            # right now, sentiment is not being taken for training
            # however, system exists where SentiStrength will be used if conditional is removed (and training)
            self.sentiment = self._sentiment(training)
            self.is_negative = is_negative(self.sentiment)
            self.is_positive = is_positive(self.sentiment)

    def to_dict(self):
        return self.__dict__

    def _sentiment(self, sentis):
        # if training, use higher-quality sentiment
        return sentistrength(self.clean) if sentis else textblob(self.clean)


class Tweet(SocialContent):
    """A tweet
       holds basic attributes and finds sentiment.
    """

    def __init__(self, j, training=False):
        dirty = j['text']
        SocialContent.__init__(self, self._clean(dirty), dirty, training=training)

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

    def __init__(self, j, training=False):
        dirty = j['commentBody']
        SocialContent.__init__(self, self._clean(dirty), dirty, training)

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

    def __init__(self, j, training=False):
        self.lead = j['lead_paragraph']
        self.abstract = j['abstract']
        self.title = j['headline']['main']
        self.source = j['source']
        self.byline = j['byline']['original'] if (j['byline']) else None
        self.abstract = self._no_html_ab()
        self.url = j['web_url']
        self.xlarge = 'https://www.nytimes.com/%s' % j['multimedia'][1]['url'] if len(j['multimedia']) > 1 else None
        self.published = j['pub_date'][:10]
        self.full = self._full_text(training)
        self.training = training
        if training:
            sw = set(stopwords.words('english'))
            mod_tit = ' '.join(filter(lambda x: x not in sw,
                                      self.title.split()))
            self.queried_title = mod_tit
            self.title_tweets = twitter_search(mod_tit, training=training)
            self.comments = article_comments(self.url, training=training)
            # notice that this count doesn't include tweets
            self.n_comments = len(self.comments)

    def to_dict(self):
        if self.full is not None and len(self.full) != 0:
            if self.training:
                self.title_tweets = map(lambda x: x.to_dict(), self.title_tweets)
            return self.__dict__
        else:
            return None

    def _no_html_ab(self):
        return BeautifulSoup(self.abstract or self.lead, 'html.parser').getText()

    def _full_text(self, training):
        """NYT url --> full article text
        """
        if 'Paid Notice:' in self.title or 'video/multimedia' in self.url:
            return None
        jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        response = opener.open(urllib2.Request(self.url))
        soup = BeautifulSoup(response.read(), 'html.parser')
        body = soup.findAll('p', {
            'class' : ['story-body-text', 'story-content']
        })
        # we'll split into paragraphs for easier reading if training
        res = ('|*^*|' if training else ' ').join(p.text for p in body)
        jar.clear()
        return res


def nyt_query_date(s):
    return s.strftime('%Y%m%d')


def article_search(keyword, training=False):
    """Get articles based on keyword."""
    # tweets are < 10 days old; articles should match
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=11)

    params = urllib.urlencode({
        'q': keyword,
        'begin_date': nyt_query_date(last_week),
        'end_date': nyt_query_date(today),
        'api-key': NYT_ARTICLE_SEARCH_KEY,
        'facet_field': 'source'
    })

    response = urllib2.urlopen('%s%s' % (ARTICLE_SEARCH_BASE, params))
    # an Article will be None if it doesn't have body text (thus the partial)
    # return an array of Article objects that have a body text
    return filter(partial(is_not, None),
                  map(lambda x: Article(x, training=training),
                      json.loads(response.read())['response']['docs']))


def article_comments(url, offset=0, training=False):
    """Gets comments for NYT times article given URL.
    """
    comments = []

    curr_key = 0
    for i in xrange(MAX_ATTEMPTS):
        if MAX_COMMENTARY < len(comments):
            break

        params = urllib.urlencode({
            'url': url,
            'api-key': NYT_COMMUNITY_KEYS[curr_key],
            'offset': i * 25
        })

        try:
            response = urllib2.urlopen('%s%s' % (COMMENT_BASE, params))
        except urllib2.HTTPError:
            # max requests exceeded (>5k queries or >30 / second)
            curr_key += 1
            i -= 1
            break


        try:
            comment_batch = json.loads(response.read())['results']['comments']
        except ValueError:
            # no json could be decoded
            break

        comments += map(lambda x: Comment(x, training=training).to_dict(),
                        comment_batch)

    return comments


def twitter_search(keyword, training=False):
    """Provide keyword for twitter search.
    Will return <= MAX_COMMENTARY tweets queried with MAX_ATTEMPTS.
    """
    twitter = get_auth()
    tweets = []

    kwargs = {
        'q': keyword,
        'lang': 'en',
        'count': 100,
        'include_entities': True
    }

    # vary API credentails to avoid rate limits
    # start with 1st combination
    curr_comb = 0
    for i in xrange(MAX_ATTEMPTS):
        if MAX_COMMENTARY < len(tweets):
            break

        try:
            response = twitter.search(**kwargs)
        except:
            # bad form but a variety of errors could be thrown
            # from exceeded rate limits
            curr_comb += 1
            twitter = get_auth(curr_comb)
            i -= 1
            continue

        tweets += map(lambda x: Tweet(x, training=training), response['statuses'])

        try:
            next_res = response['search_metadata']['next_results']
            next_max = next_res.split('max_id=')[1].split('&')[0]
            kwargs['max_id'] = next_max
        except KeyError:
            # no more results
            break

    return tweets


def get_auth(comb=0):
    auth = Twython(TWITTER_KEYS[comb], TWITTER_SECRETS[comb], oauth_version=2)
    return Twython(TWITTER_KEYS[comb], access_token=auth.obtain_access_token())
