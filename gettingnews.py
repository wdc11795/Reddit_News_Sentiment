from bs4 import BeautifulSoup
import datetime
import pickle
import requests
import random

# PARAMETERS
# stock
FNAME = "snp500_formatted.txt"
stocks = []
with open(FNAME) as f:
    stocks = f.readlines()
for i in range(len(stocks)):
    stocks[i] = stocks[i].rstrip('\n')
# stocks = ["MSFT", "GOOGL", "AAPL", "TSLA", "WDC", "RAD", "BAC", "F", "GE", "T", "M", "WFC", "JCP", "KR", "GM", "KO", "DIS", "SWN", "PFE", "WMT" ]
stocks = ['AAPL', 'FB', 'GOOGL', 'TSLA', 'AMZN', 'TSLA', 'BKRB', 'JNJ']

# time period
time_period = 14

# how many days ago should I start at
starting_date = -365 * 7 + -337


def getNewsForWeek(date):
    thedate = date
    print("important:" + thedate.strftime('%Y-%m-%d'))
    file = open('../data/news/' + thedate.strftime('%Y-%m-%d') + '.csv', 'w')
    file.write("Ticker,Headlines")
    file.write('\n')

    print("FILE:" + 'data/news/' + thedate.strftime('%Y-%m-%d') + '.csv', 'w')
    for i in range(len(stocks)):
        allnews = ""
        for j in range(time_period):
            thedate = date
            thedate += datetime.timedelta(days=j)
            # print('Getting news for ' + thedate.strftime('%Y-%m-%d'))
            query = 'http://www.reuters.com/finance/stocks/company-news/' + stocks[i] + '.O' + '?date=' + format(
                thedate.month, '02d') + format(thedate.day, '02d') + str(thedate.year)
            # print(query)
            # print('Getting news for ' + stocks[i])

            response = requests.get(query)
            soup = BeautifulSoup(response.text, "html.parser")
            divs = soup.findAll('div', {'class': 'feature'})
            divs2 = soup.findAll('div', {'class': 'topStory'})
            # print('Found ' + str(len(divs) + len(divs2)) + ' articles.')

            if (len(divs) == 0 and len(divs2) == 0):
                continue
            # data = u''
            data = []

            for div in divs:
                test = div.findAll(text=True)[0]
                data = data + [test]
                # data = data.join(div.findAll(text=True))
            # news = data.split('\n')[0]
            # news = news.strip().replace(',','')
            news = data

            data2 = u''

            for div in divs2:
                data2 = data2.join(div.findAll(text=True))

            news2 = data2
            news2 = news2.replace('\n', "--")
            test = news2.split("--")
            for j in range(len(test)):
                if test[j] != "" and test[j] != "Continue Reading":
                    news2 = test[j]
                    break

            news = news + [news2]
            for k in range(len(news)):
                news[k] = news[k].replace(",", "")
            news = "|".join(news)
            # print(news)
            # news = data.strip().split('\n')
            # news = data.strip().replace('\n',' ').split(' ')
            # news = " ".join(news)
            allnews = allnews + "|" + news

        # print(allnews)
        file.write(stocks[i] + ',' + allnews[1:])
        file.write('\n')
        thedate += datetime.timedelta(days=-time_period)
    file.close()

    def getNews():
        endDate = datetime.date.today()
        date = endDate
        date += datetime.timedelta(days=starting_date)
        print(date)
        while (date <= endDate):
            getNewsForWeek(date)
            date += datetime.timedelta(days=time_period)
            getNews()
