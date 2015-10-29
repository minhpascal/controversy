# -*- coding: utf-8 -*-
"""
    scoring.py
    ~~~~~~~~~~

    Scores controversy given articles and tweets corpora.

    :authors: Ismini Lourentzou, Graham Dyer
"""
import math
import nltk
import string
import scipy
import heapq
import re
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from content import Tweet, Article
from lexicon_extreme import is_extreme
from collections import namedtuple


stemmer = PorterStemmer()
X_s = namedtuple('X_s', 'feature sentiment')


class BM25:
    def __init__(self, fn_docs, delimiter='|'):
        self.dictionary = corpora.Dictionary()
        self.DF = {}
        self.delimiter = delimiter
        self.DocTF = []
        self.DocIDF = {}
        self.N = 0
        self.DocAvgLen = 0
        self.fn_docs = fn_docs
        self.DocLen = []
        #self.raw_data = []
        self.build_dictionary()
        self.tf_idf_generator()


    def build_dictionary(self):
        proc_data = []
        for i in xrange(len(self.fn_docs)):
            tweet = self.fn_docs[i].clean_tweet
            # sentiment = self.fn_docs[i]["sentiment"]
            # self.raw_data.append(self.fn_docs[i])
            proc_data.append(preprocess(tweet))
        self.dictionary.add_documents(proc_data)


    def tf_idf_generator(self, base=math.e):
        docTotalLen = 0.0
        # print (self.dictionary.token2id)
        for i in xrange(len(self.fn_docs)):
            tweet = self.fn_docs[i].clean_tweet
            doc = preprocess(tweet)
            docTotalLen += len(doc)
            self.DocLen.append(len(doc))
            # print self.dictionary.doc2bow(doc)
            bow = dict([(term, freq * 1.0 / len(doc)) for term, freq in self.dictionary.doc2bow(doc)])
            for term, tf in bow.items():
                if term not in self.DF:
                    self.DF[term] = 0
                self.DF[term] += 1
            self.DocTF.append(bow)
            self.N = self.N + 1
        for term in self.DF:
            self.DocIDF[term] = abs(math.log( (self.N - self.DF[term] + 0.5) / (self.DF[term] + 0.5), base))
            # negative IDF hits on my nerves! Aaaaaaaarg!
        self.DocAvgLen = docTotalLen / self.N


    def bm25_score(self, Query=[], k1=1.2, b=0.75):
        query_bow = self.dictionary.doc2bow(Query)
        scores = []
        for idx, doc in enumerate(self.DocTF):
            commonTerms = set(dict(query_bow).keys()) & set(doc.keys())
            tmp_score = []
            doc_terms_len = self.DocLen[idx]
            for term in commonTerms:
                upper = (doc[term] * (k1 + 1))
                below = ((doc[term]) + k1 * (1 - b + b * doc_terms_len / self.DocAvgLen))
                tmp_score.append(self.DocIDF[term] * upper / below)
            score = sum(tmp_score)
            if score!=0:
                scores.append((score, idx))
        return sorted(scores, reverse=True) # descending order


    def tf_idf(self):
        tfidf = []
        for doc in self.DocTF:
            doc_tfidf  = [(term, tf * self.DocIDF[term]) for term, tf in doc.items()]
            # print doc, tf, self.DocIDF[term]
            doc_tfidf.sort()
            tfidf.append(doc_tfidf)
        # print "tfidf:", tfidf
        return tfidf


    def items(self):
        # return a list [(term_idx, term_desc),]
        it = self.dictionary.items()
        it.sort()
        return it


def preprocess(file_content):
    tot_tokens = []
    file_content = file_content.lower()
    # remove odd chars
    file_content = re.sub(r'[^a-z0-9 ]', ' ', file_content)
    # remove punctuation
    file_content = re.sub('[%s]' % re.escape(string.punctuation), '', file_content)
    # tokenization
    file_content = nltk.word_tokenize(file_content)
    tot_tokens.append(len(file_content))
    # stemming + count term frequency
    stemmed_Words = []
    for word in file_content:
        if word not in stopwords.words('english'):
            stemmedWord = word
            stemmed_Words.append(stemmedWord)
    return stemmed_Words


def score_entropy(li):
    """Get entropy of list ``li``.
    """
    ret = dict((x, (li.count(x) / float(len(li)))) for x in set(li)).values()
    #ret = map(lambda x: li.count(x) / float(len(li)), li)
    return scipy.stats.entropy(ret, base=2)


def sentiments_of_i(i, C):
    res = len(filter(lambda x: x.sentiment == i, C))
    """$p(X_{sent} = x_i) = number of tweets
    with sentiment $x_i$ / total number of comments C.
    Provides number of tweets in corpus C with sentiment i
    """
    return res


def sentiment_conditional(l):
    res = []
    for i in xrange(-4, 4):
        count_xi = sentiments_of_i(i, l)
        if (count_xi == 0):
            res.append(0)
        else:
            res.append(float(sentiments_of_i(i, filter(lambda x: x.feature == True, l))) / float(count_xi))
    return res
     

def controversy(articles, tweets):
    bm25 = BM25(tweets, delimiter=' ')
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    article_count = len(articles)
    ranked_articles = [{}] * article_count

    # for every article matching the keyword
    for article_index in xrange(article_count):
        dict_art = articles[article_index].to_dict()
        if (dict_art is None):
            continue

        ranked_articles[article_index] = dict_art
        sentiment_score, linguistic_score = 0, 0 # (entropy) score of the entire article
        sentences = [] # scores & metadata for each sentence
        query = tokenizer.tokenize(articles[article_index].full)

        # for every sentence in the article
        for sentence in query:
            scores = bm25.bm25_score(preprocess(sentence))
            sentiments, extremes, caps, relevant_tweets = [], [], [], []

            # for every tweet relevant to the sentence
            for tweet in scores:
                # get the index of the relevant tweet
                doc_index = tweet[1]
                relevant_tweet = tweets[doc_index]
                sentiment = relevant_tweet.sentiment
                sentiments.append(sentiment)

                words = relevant_tweet.clean_tweet.split(' ')
                extreme_words_count = sum(map(lambda x: int(is_extreme(x)), words))
                extremes.append(X_s(extreme_words_count > 0, sentiment))

                # p(X_caps = x_i) = p(X_sent = x_i | C'_i \in Caps)

                caps_count = sum(map(lambda x: int(x.isupper()), words))
                caps.append(X_s(caps_count > 0, sentiment))

                # save tweet for json response
                relevant_tweets.append(relevant_tweet.to_dict())


            sentence_sentiment_score = score_entropy(sentiments)
            sentiment_score += sentence_sentiment_score
            
            extreme_score = score_entropy(sentiment_conditional(extremes))
            caps_score = score_entropy(sentiment_conditional(caps))

            sentence_linguistic_score = caps_score + extreme_score
            linguistic_score += sentence_linguistic_score

            sentences.append({
                'tweets': relevant_tweets,
                'text': sentence,
                'score': linguistic_score + sentiment_score,
                'linguistic_score': linguistic_score,
                'sentiment_score': sentiment_score
            })
        # 15% of the sentence count
        n = int(math.ceil(len(sentences) * 0.15))
        # n (15%) largest scores (recall greater entropy ==> more controversial)
        nlargest = heapq.nlargest(n, map(lambda x: x['score'], sentences))
        # only provide controversial sentences with "enough" related tweets
        filtered = filter(lambda x: any(x['score'] >= i for i in nlargest) and len(x['tweets']) > 5, sentences)

        ranked_articles[article_index].update({
            'sentences': filtered,
            'linguistic_score': linguistic_score,
            'sentiment_score': sentiment_score,
            'score': linguistic_score + sentiment_score
        })

    ranked_articles = filter(lambda x: 'score' in x, ranked_articles)

    # sort in order of decreasing entropy (most controversial --> least)
    return sorted(ranked_articles,
                  key=lambda x: x['score'],
                  reverse=True)
