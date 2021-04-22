from bs4 import BeautifulSoup
import datetime
import pickle
import requests
import random
import numpy as np
import pandas as pd


#parameters
#how many days ago should I start from
starting_date = -518


def getNewsForWeek(date):
    thedate = date
    thedate = date
    query = "https://web.archive.org/web/" +  str(thedate.year) +  format(thedate.month, '02d') +  format(thedate.day, '02d') + "/http://www.reddit.com/r/worldnews/"

    response = requests.get(query)
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.findAll('p', {'class': 'title'})

    data = []

    for div in divs:
        test = div.findAll(text=True)
        test = (max(test, key=len))
        data = data + [test]
    return data


empty = pd.DataFrame([])
endDate = datetime.date.today()
date = endDate
date += datetime.timedelta(days=  starting_date)
while(date <= endDate):
    data = getNewsForWeek(date)
    #print(date, len(data))
    empty = empty.append(pd.DataFrame({'date': date, "headlines": [data]}, index=[0]), ignore_index=True)
    date += datetime.timedelta(days=1)


empty

headlines_df = empty

headlines_df.head()

test_df = headlines_df['headlines'].apply(pd.Series)
test_df.index = headlines_df['date']
test_df.head()

test_df.to_csv("remainingreddit.csv")

