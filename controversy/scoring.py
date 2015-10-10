# -*- coding: utf-8 -*-
"""
    scoring.py
    ~~~~~~~~~~

    Scores controversy given articles and tweets corpora.

    :authors: Ismini Lourentzou, Graham Dyer
"""
import math, nltk, re, string, scipy, heapq
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from content import Tweet, Article
from lexicon_extreme import is_extreme


stemmer = PorterStemmer()


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
    ret = map(lambda x: li.count(x) / float(len(li)), li)
    return scipy.stats.entropy(ret, base=2)



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
        score, sentiment_score, linguistic_score = 0, 0, 0 # (entropy) score of the entire article
        sentences = [] # scores & metadata for each sentence
        query = tokenizer.tokenize(articles[article_index].full)

        # for every sentence in the article
        for sentence in query:
            scores = bm25.bm25_score(preprocess(sentence))
            sentiments, extremes, relevant_tweets = [], [], []

            # for every tweet relevant to the sentence
            for tweet in scores:
                # get the index of the relevant tweet
                doc_index = tweet[1]
                relevant_tweet = tweets[doc_index]
                sentiments.append(relevant_tweet.sentiment)

                extreme_words_count = reduce(lambda x, y: is_extreme(x) + is_extreme(y), relevant_tweet.clean_tweet.split(' '))
                extremes.append(extreme_words_count)

                relevant_tweets.append(relevant_tweet.to_dict())

            #sentiments = dict((x, (sentiments.count(x) / float(len(sentiments)))) for x in set(sentiments)).values()
            sentence_sentiment_score = score_entropy(sentiments)
            sentiment_score += sentence_sentiment_score

            sentence_linguistic_score = score_entropy(extremes) # will add all-caps soon
            linguistic_score += sentence_linguistic_score

            score += (sentence_sentiment_score + sentence_linguistic_score)

            sentences.append({
                'tweets': relevant_tweets,
                'text': sentence,
                'score': linguistic_score + sentiment_score,
                'linguistic_score': linguistic_score,
                'sentiment_score': sentiment_score
            })

        # 6% of the sentence count
        n = int(math.ceil(len(sentences) * 0.06))
        # n largest (top 6%) scores (recall greater entropy ==> more controversial)
        nlargest = heapq.nlargest(n, map(lambda x : x['score'], sentences))
        # only provide controversial sentences with "enough" related tweets
        filtered = filter(lambda x: any(x['score'] >= i for i in nlargest) and len(x['tweets']) > 5, sentences)

        print(ranked_articles[article_index])
        ranked_articles[article_index]['sentences'] = filtered
        ranked_articles[article_index]['score'] = score

    with open('tmp.json', 'w') as f:
        import json
        f.write(json.dumps(ranked_articles))


    # sort in order of decreasing entropy (most controversial --> least)
    return sorted(ranked_articles,
                  key=lambda x: x['score'],
                  reverse=True)
