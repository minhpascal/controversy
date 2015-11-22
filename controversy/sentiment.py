# -*- coding: utf-8 -*-
"""
    sentiment.py
    ~~~~~~~~~~~~

    Sentiment of a string.
    Both TextBlob and SentiStrength are available.
"""
from textblob import TextBlob
import shlex
import subprocess


def textblob(tweet):
    """score with TextBlob.
    """
    blob = TextBlob(tweet)
    res = int(blob.sentiment.polarity * 4)
    return res


def is_negative(val):
    #return val < 1.75
    return val < 0


def is_positive(val):
    #return val > 2.25
    return val > 0


def sentistrength(s):
    """Score with SentiStength
    """
    p = subprocess.Popen(shlex.split('java -jar sentistrength/SentiStrengthCom.jar stdin sentidata sentistrength/data-11/ scale'), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s = s.encode('utf8')
    stdout_text, stderr_text = p.communicate(s.replace(' ', '+'))
    try:
        return int(float(stdout_text.rstrip().split('\t')[-1]))
    except ValueError:
        return 0
