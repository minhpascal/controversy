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


def analyse(tweet):
    """score with TextBlob -- currently the default
    """
    blob = TextBlob(tweet)
    # [0, 4]
    return (blob.sentiment.polarity + 1) * 2


def is_negative(val):
    return val < 1.75


def is_positive(val):
    return val > 2.25


def sentistrength(s):
    """score with sentistength
    """
    p = subprocess.Popen(shlex.split('java -jar sentistrength/SentiStrengthCom.jar stdin sentidata sentistrength/data-11/'), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_text, stderr_text = p.communicate(s.replace(' ','+'))
    stdout_text = stdout_text.rstrip().replace('\t','')
    return stdout_text
