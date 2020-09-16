import datetime
import os
import sys
import logging
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

from common.Mongo_client import Mongo
from common.AMQP_client import AMQPClient
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

DEDUPE_NEWS_TASK_QUEUE_NAME = "top-new-DEDUPE_NEWS_TASK_QUEUE_NAME"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

mongoDB = Mongo().get_collection()


def handle_message(message):
    if not isinstance(message, dict):
        return
    text = message['text']
    if text is None:
        return
    published_at = parser.parse(message['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    same_day_news_list = list(mongoDB.find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))
    Logger.info('Length of previous news: {}'.format(len(same_day_news_list)))
    message['publishedAt'] = published_at
    mongoDB.replace_one({'digest': message['digest']}, message, upsert=True)
    Logger.info('Succefully insert news: {}'.format(message['title']))



amqp_client = AMQPClient(queue_name=DEDUPE_NEWS_TASK_QUEUE_NAME, callBack=handle_message)
amqp_client.receiveMessage()
