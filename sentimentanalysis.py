from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata
sid = SentimentIntensityAnalyzer()
import pandas as pd
import numpy as np
import os


path = "../data/news/"
files = [file_path for file_path in os.listdir(path) if file_path.endswith('.csv')]
finalpath = "../data/sentiments/"
for fname in files:
    print(fname)
    df = pd.read_csv(path + fname)
    df['polarity'] = 0
    df['max_polarity'] = 0
    df['subjectivity'] = 0
    df['pos'] = 0
    df['neu'] = 0
    df['neg'] = 0
    for ind, row in df.iterrows():
        if type(row['Headlines']) != str :
            df.loc[ind, 'polarity'] = 0
            df.loc[ind, 'subjectivity'] = 0
            df.loc[ind, 'pos'] = 0
            df.loc[ind, 'neg'] = 0
            df.loc[ind, 'neu'] = 0
        else:
            headlines = row['Headlines']
            headlines = headlines.split("|")
            polarity = [ TextBlob(headline).sentiment.polarity for headline in headlines]
            mostExtreme = -99999
            for  val in polarity:
                if abs(val) > mostExtreme:
                    mostExtreme = val
            sslist = [sid.polarity_scores(headline) for headline in headlines]
            subjectivity = [ TextBlob(headline).sentiment.subjectivity for headline in headlines]
            positives = [ss['pos'] for ss in sslist]
            negatives = [ss['neg'] for ss in sslist]
            neutrals = [ss['neu'] for ss in sslist]
            df.loc[ind, 'polarity'] = np.mean(polarity)
            df.loc[ind, 'subjectivity'] = np.mean(subjectivity)
            df.loc[ind, 'max_polarity'] = mostExtreme
            df.loc[ind, 'pos'] = np.mean(positives)
            df.loc[ind, 'neu'] = np.mean(neutrals)
            df.loc[ind, 'neg'] = np.mean(negatives)


            print(np.mean(polarity), np.mean(subjectivity), mostExtreme, np.mean(positives), np.mean(neutrals), np.mean(negatives))
    df.to_csv(finalpath+fname)

finalpath = "../data/sentiments/"
stockpath = "../data/stock_sentiment"
files = [file_path for file_path in os.listdir(finalpath) if file_path.endswith('.csv')]
file_names = [file.split('.')[0] for file in files]
stocks = ["MSFT", "GOOGL", "AAPL", "TSLA", "WDC", "RAD", "BAC", "F", "GE", "T", "M", "WFC", "JCP", "KR", "GM", "KO",
          "DIS", "SWN", "PFE", "WMT"]
stocks = ["AAPL", "MSFT", "GOOGL", "TSLA"]
stocks = ['AAPL', 'FB', 'GOOGL', 'TSLA', 'AMZN', 'TSLA', 'BKRB', 'JNJ']

sentiments = ['polarity', 'subjectivity', 'max_polarity', 'pos', 'neg', 'neu']
for stock in stocks:
    df = pd.DataFrame(index=file_names, columns=sentiments)
    # print(df.head())

    for ind, fname in enumerate(files):
        date = fname.split('.')[0]
        stock_df = pd.read_csv(finalpath + fname)
        if (len(df) != 0):
            if len((stock_df[stock_df['Ticker'] == stock][sentiments]).values) != 0:
                df.loc[date, :] = ((stock_df[stock_df['Ticker'] == stock][sentiments]).values[0])
    df.to_csv(stockpath + '/' + stock + '.csv')

finalstocks = ['AAPL', "AMZN", "FB", "GOOGL", "TSLA"]
paths = [stockpath + '/' + stock + ".csv" for stock in finalstocks]
newpath = [stockpath + '/' + stock + "interpolate" +".csv" for stock in finalstocks]
paths

for ind, path in enumerate(paths):
    df = pd.read_csv(path)
    df = df.replace(0, np.nan)
    df = df.interpolate()
    df.to_csv(newpath[ind])