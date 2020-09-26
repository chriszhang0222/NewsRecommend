import datetime
import hashlib
import redis
import json
import logging
import os
import sys
from newspaper import Article

from common.NewsService import getNewsFromSource, getNewsWithTopic, fetch_news_top_us
from common.AMQP_client import AMQPClient
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)


SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
SCRAPE_NEWS_TASK_QUEUE_NAME = "top-news-SCRAPE_NEWS_TASK_QUEUE"

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=8)
amqp_client = AMQPClient(SCRAPE_NEWS_TASK_QUEUE_NAME)


def start_fetching():
    Logger.info('Start Fetching...')
    news_list = fetch_news_top_us()
    num_of_news = 0
    for news in news_list:
        if news['title'] is None:
            continue
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
        if redis_client.get(news_digest) is None:
            num_of_news += 1
            news['digest'] = news_digest
            if news.get('publishedAt', None) is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            redis_client.set(news_digest, news['title'])
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)
            amqp_client.sendMessage(news)
    amqp_client.sleep(SLEEP_TIME_IN_SECONDS)

    Logger.info('Fetch news count: {}'.format(num_of_news))


if __name__ == '__main__':
    while True:
        start_fetching()




