from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata
sid = SentimentIntensityAnalyzer()
import pandas as pd
import numpy as np
import os
import re


df = pd.read_csv("remainingreddit.csv", encoding = 'latin1')
df=df.rename(columns = {'Unnamed: 0':'Date'})
columns = df.columns.values.tolist()
df = df.loc[:,columns]
print(df.columns)
df.tail()


headlines = columns
headlines.remove('Date')


reddit_df = pd.DataFrame(np.nan, index=df['Date'], columns=['neg', 'neu', 'pos', 'polarity', 'subjectivity'])
reddit_df


sentiment_df = df

for ind, row in sentiment_df.iterrows():
    pos = []
    neg = []
    neu = []
    polarity = []
    subjectivity = []
    for headline in headlines:
        test = sentiment_df.iloc[ind][headline]
        print(test)
        print(type(test) == type(""))
        if (type(test) == type("")):
            test = re.sub(r'([^\s\w]|_)+', '', sentiment_df.iloc[ind][headline]).strip()[1:]
            sentiment = TextBlob(test).sentiment.polarity
            sentiment1 = TextBlob(test).sentiment.subjectivity
            ss = sid.polarity_scores(test)
            print(ss)
            pos = pos + [ss['pos']]
            neg = neg + [ss['neg']]
            neu = neg + [ss['neu']]
            polarity = polarity + [sentiment]
            subjectivity = subjectivity + [sentiment1]

    reddit_df.set_value(row["Date"], 'neg', np.mean(neg))
    reddit_df.set_value(row["Date"], 'pos', np.mean(pos))
    reddit_df.set_value(row["Date"], 'neu', np.mean(neu))
    reddit_df.set_value(row["Date"], 'polarity', np.mean(polarity))
    reddit_df.set_value(row["Date"], 'subjectivity', np.mean(subjectivity))

test_df = reddit_df

idx = pd.date_range('2016-07-02', '2017-11-23')
test_df.index = pd.DatetimeIndex(test_df.index)
test_df = test_df.reindex(idx, fill_value=np.nan)
test_df.head()

test_df

test_df = test_df.reset_index()
columns = test_df.columns.values.tolist()
test_df = test_df.loc[:,columns]
test_df.head()

analysis_df = test_df.groupby(np.arange(len(test_df))//7).mean()


analysis_df.to_csv("reddit_five_sentimentslastyear.csv")


reddit_df.tail()