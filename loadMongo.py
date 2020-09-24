from common.Mongo_client import Mongo
import csv
"""
NBA: 1
covid-19: 2
other sports: 3
Trump: 4
"""
mongo = Mongo()
collections = mongo.get_db().get_collection('news')

BASKET_BALL = [
    'NBA', 'Lebron', 'playoffs', 'Nuggets', 'Lakers', 'basketball', 'Clippers', 'playoffs',
    'Harden', 'Rockets', ''
]
with open("labeled_news.csv", "a") as f:
    csv_writer = csv.writer(f)
    for x in collections.find():
        title = x['title']
        desc = x['description']
        title.replace(',', '\\,')
        desc.replace(',', '\\,')
        source = x['source']
        url = x['url']
        if x['source'].lower() == 'espn' or x['source'] == 'espn':
            isBasket = False
            for basket in BASKET_BALL:
                if basket in title or basket in desc:
                    isBasket = True
                    break
            if 'nba' in url:
                isBasket = True
            if isBasket:
               csv_writer.writerow([1, title, desc, source])
            else:
                csv_writer.writerow([3, title, desc, source])
        elif 'covid' in x['title'] or 'covid' in x['description'] or 'covid' in x['text'] or 'Coronavirus' in x['title']:
            csv_writer.writerow([2, title, desc, source])
        elif 'Trump' in x['title'] or 'Trump' in x['description']:
            csv_writer.writerow([4, title, desc, source])

# import pandas as pd
#
# DATA_SET_FILE = './labeled_news.csv'
#
# df = pd.read_csv(DATA_SET_FILE, header=None)