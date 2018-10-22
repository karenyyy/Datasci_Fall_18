import pandas as pd
from textblob import TextBlob
import re
import numpy as np


def process_text(data):
    cleaned_text = [
        re.sub('\s+', ' ', re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", '',
               tweets.lower()).strip()) for tweets in data
    ]
    return cleaned_text


tweet = pd.read_csv('data_2018-08-28_15-56-07.csv', sep=',')


tweet['text'] = process_text(tweet['text'])

sentiment = []
for i in tweet['text']:
    print(i)
    s = TextBlob(i).sentiment
    polarity = s.polarity
    subj = s.subjectivity

    if subj < 0.05 and polarity < 0.1 and 'mccain' not in i.lower():
        sentiment.append('irrelevant')
    else:
        if polarity > 0:
            sentiment.append('positive')
        elif polarity < 0:
            sentiment.append('negative')
        else:
            sentiment.append('neutral')

    print(sentiment[-1])

tweet['sentiment'] = pd.Series(sentiment, name='sentiment')

tweet.to_csv('cleaned_tagged.csv', sep=',')
