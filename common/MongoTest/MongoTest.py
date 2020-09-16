from common.NewsService import getNewsFromSource
from common.Mongo_client import Mongo
from dateutil import parser
mongo = Mongo()
news = getNewsFromSource()

for new in news:
    i = 0
    print(news)