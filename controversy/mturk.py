# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session, render_template
from functools import wraps
from digest import digest
from pymongo import MongoClient
from config import MONGO_PORT
import content
import datetime
import time
import forms
from error import UsageError
import nltk.data
import itertools
from nltk.tokenize import RegexpTokenizer


mturk = Blueprint('/training', __name__)
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
tokenizer = RegexpTokenizer(r'\w+')


def require_human(view):
    @wraps(view)
    def protected_view(*args, **kwargs):
        if is_human():
            return view(*args, **kwargs)
        else:
            raise UsageError('not human!')
    return protected_view


def is_human():
    return session.get('human') == 'yes'


def success():
    return jsonify({
        'ok': 1
    })


@mturk.errorhandler(UsageError)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@mturk.route('/', methods=['GET', 'POST'])
def index():
    css = digest('mturk/highlight.css')
    js = digest('mturk/highlight.js')
    if not is_human():
        form = forms.BeginHIT()
        if form.validate_on_submit():
            session['human'] = 'yes'
        else:
            return render_template('mturk_welcome.html',
                                   form=form,
                                   css=css,
                                   js=js)

    article = get_next_doc()
    if article is None:
        return render_template('mturk_no_tasks.html',
                               css=css)

    n_sentences = len(article['full'])
    # minimum reading time in milliseconds (at 750 wpm, fast skimming pace)
    minimum_time = int(100 * (float(60 * len(tokenizer.tokenize(article['full']))) / 75))

    # split by paragraph and then sentences
    paras = map(lambda x: sent_detector.tokenize(x.strip()), article['full'].split('|*^*|'))
    article['full'] = list(itertools.chain(*paras))
    # not the cleanest solution for paragraphs, but it'll be fine
    sentence_lookup = lambda x: article['full'].index(x)

    session['minimum_time'] = minimum_time
    session['started_reading'] = time.time()
    session['n_sentences'] = sum(map(lambda x: len(x), article['full']))
    session['reading_url'] = article['url']

    return render_template('mturk_highlight.html',
                           css=css,
                           js=js,
                           minimum_time=minimum_time,
                           n_sentences=n_sentences,
                           paras=paras,
                           sentence_lookup=sentence_lookup,
                           article=article)


@mturk.route('/mark_available')
@require_human
def mark_available():
    toggle_being_read(get_articles_collection(),
                      session['reading_url'],
                      False)
    return success()


@mturk.route('/submit', methods=['GET', 'POST'])
@require_human
def update_doc():
    if 'checked' not in request.args:
        raise UsageError('missing ``checked`` arg!')

    inds = request.args['checked'].split(',')
    n_inds = len(inds)
    if time.time() - session['started_reading'] < (float(session['minimum_time']) / 1000):
        raise UsageError('reading speed too fast')

    if n_inds > session['n_sentences'] or n_inds < 1:
        raise UsageError('no or too many highlights')

    col = get_articles_collection()
    url = session['reading_url']
    increment_reads(col, url, inds)
    toggle_being_read(col, url, False)

    return success()


@mturk.route('/submitted')
@require_human
def submitted():
    css = digest('mturk/highlight.css')
    return render_template('mturk_submitted.html', **locals())


def get_db():
    client = MongoClient('localhost', MONGO_PORT)
    return client.controversy


def get_articles_collection():
    return get_db().articles


def get_tweets_collection():
    return get_db().tweets


def increment_reads(col, url, highlights):
    return col.update_one({
        'url': url
    }, {
        '$set': {
            'ts': datetime.datetime.utcnow()
        }, '$inc': {
            'n_reads': 1
        }, '$push': {
            'highlights': highlights
        }
    }).modified_count


def toggle_being_read(col, url, dest):
    return col.update_one({
        'url': url
    }, {
        '$set': {
            'being_read': dest
        }
    })


def new_doc(doc):
    """given an API response, make an entry for each article,
    preserving the timestamp of the entire response and keyword.
    Cache tweets by keyword (not associated with article corpus for speed).
    Returns number of articles found.
    """
    if doc['ok'] != 1:
        return 0

    ar_col = get_articles_collection()
    tw_col = get_tweets_collection()
    res = doc['result']
    
    tw_col.insert_one({
        'tweets': res['kw_tweets'],
        'ts': doc['ts'],
        'keyword': doc['ts']
    })

    n_docs = 0
    for article in res['articles']:
        if article is None:
            continue
        n_docs += 1
        a = {
            'ts': doc['ts'],
            'keyword': doc['keyword'],
            'n_reads': 0,
            'being_read': False,
            'highlights': []
        }
        a.update(article)
        ar_col.insert_one(a).inserted_id
    return n_docs


def get_next_doc():
    col = get_collection()
    poss = col.find({
        'n_reads' : {
            '$lt': 3
        }
    }).sort([
        ('being_read', 1)
    ])

    if poss is None:
        return None

    try:
        to_be_read = poss[:][0]
    except IndexError:
        return None
    toggle_being_read(col, to_be_read['url'], True)
    return to_be_read
