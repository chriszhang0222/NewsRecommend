import datetime
import hashlib
import redis
import json
import logging
import os
import sys
from newspaper import Article

from common.NewsService import getNewsFromSource
from common.AMQP_client import AMQPClient
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)


SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
SCRAPE_NEWS_TASK_QUEUE_NAME = "top-news-SCRAPE_NEWS_TASK_QUEUE"

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=8)

url = 'http://us.cnn.com/2020/09/15/health/us-coronavirus-tuesday/index.html'
article = Article(url)
article.download()
article.parse()
print(article.text)

