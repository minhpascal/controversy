# -*- coding: utf-8 -*-
"""
    scoring.py
    ~~~~~~~~~~
    Adds score and relevant tweets to response.
    :authors: Ismini Lourentzou, Graham Dyer

    *to be optimized soon*
"""
import math, nltk, re, string, scipy, heapq
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from content import Tweet, Article


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
            tweet = self.fn_docs[i]['clean_tweet']
            # sentiment = self.fn_docs[i]["sentiment"]
            # self.raw_data.append(self.fn_docs[i])
            proc_data.append(preprocess(tweet))
        self.dictionary.add_documents(proc_data)


    def tf_idf_generator(self, base=math.e):
        docTotalLen = 0.0
        # print (self.dictionary.token2id)
        for i in xrange(len(self.fn_docs)):
            tweet = self.fn_docs[i]['clean_tweet']
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


def controversy(data):
    bm25 = BM25(data["tweets"], delimiter=' ')
    tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

    # for every article
    for article_index in xrange(len(data['articles'])):
        entropy_sentiment_score = 0 # note that vanilla "score" is entropy
        ratio_sentiment_score = 0 # ratio score, of course
        query = tokenizer.tokenize(data['articles'][article_index]['full'])
        sentences = []

        # for every sentence
        for sentence in query:
            scores = bm25.bm25_score(preprocess(sentence))
            sentiments = []
            cap_rule = []
            extreme_rule = []
            relevant_tweets = []
            negative_tweet_count = 0
            positive_tweet_count = 0

            # for every relevant tweet
            for tweet in scores:
                doc_index = tweet[1]
                sentiments.append(data['tweets'][doc_index]['sentiment'])
                if data['tweets'][doc_index]['is_positive']:
                    positive_tweet_count += 1
                elif data['tweets'][doc_index]['is_negative']:
                    negative_tweet_count += 1
            
                relevant_tweets.append(data['tweets'][doc_index])

            # find entropy of sentiment
            sentiments = dict((x,(sentiments.count(x) / float(len(sentiments)))) for x in set(sentiments)).values()
            entropy_sentiment = scipy.stats.entropy(sentiments, base=2)
            entropy_sentiment_score += entropy_sentiment
           
            # smaller ratio ==> more controversial
            try:
                sentence_level_ratio = abs((negative_tweet_count / float(positive_tweet_count + negative_tweet_count)) - 0.5) 
            except ZeroDivisionError:
                sentence_level_ratio = 0
            ratio_sentiment_score += sentence_level_ratio

            sentences.append({
                'tweets' : relevant_tweets,
                'text' : sentence,
                'sentiment_entropy' : entropy_sentiment,
                'sentiment_ratio' : sentence_level_ratio
            })

        # 6% of the sentence count
        n = int(math.ceil(len(sentences) * 0.06))
        # create a list of n largest sentiment entropy values (recall greater entropy ==> more controversial)
        nlargest = heapq.nlargest(n, map(lambda x : x['sentiment_entropy'], sentences))
        # notice this is just filtering by sentiment entropy
        filtered = filter(lambda x : any(x['sentiment_entropy'] >= i for i in nlargest) and len(x['tweets']) > 1, sentences)



        data['articles'][article_index]['sentences'] = filtered
        data['articles'][article_index]['entropy_sentiment_score'] = entropy_sentiment_score
        data['articles'][article_index]['ratio_sentiment_score'] = ratio_sentiment_score

    data.pop('tweets', None)
    # sort in order of decreasing entropy (most controversial --> least)
    return {
        'error': 0, 
        'result': sorted(data['articles'],
                         key=lambda x: x['entropy_sentiment_score'],
                         reverse=True)
    }
