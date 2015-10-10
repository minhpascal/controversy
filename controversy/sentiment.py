# -*- coding: utf-8 -*-
"""
    sentiment.py
    ~~~~~~~~~~~~

    Sentiment of a string.

    The paper referenced SentiStrength, although we've switched to TextBlob.
"""
from textblob import TextBlob

def analyse(tweet):
    blob = TextBlob(tweet)
    #: [0, 4]
    return (blob.sentiment.polarity + 1) * 2


def is_negative(val):
    return val < 1.75


def is_positive(val):
    return val > 2.25
