from textblob import TextBlob

def analyse(tweet):
    blob = TextBlob(tweet)
    #: [0, 4]
    return (blob.sentiment.polarity + 1) * 2
