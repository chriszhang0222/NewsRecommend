import logging
import pickle
import re

import jsonrpclib
import json
import redis
from backend.client.news_recommendation_client import getPreferenceForUser
from backend.client.news_topic_client import classify
from datetime import datetime
from common.Mongo_client import Mongo
from common.AMQP_client import AMQPClient
from bson.json_util import dumps


logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

REDIS_HOST = '192.168.0.17'
REDIS_PORT = 6379

NEWS_TABLE_NAME = "news"
CLICK_LOGS_TABLE_NAME = 'click_logs'

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 60
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=8)
LOG_CLICKS_TASK_QUEUE_NAME = "LOG_CLICKS_TASK_QUEUE"


def getOneNews():
    news = Mongo.get_collection(name=NEWS_TABLE_NAME).find_one()
    return json.loads(dumps(news))


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num) * NEWS_LIST_BATCH_SIZE
    end_index = (page_num + 1) * NEWS_LIST_BATCH_SIZE

    sliced_news = []
    news_collection = Mongo().get_collection(name=NEWS_TABLE_NAME)
    preference, preference_values = getPreferenceForUser(user_id)
    topPreference = None
    secondaryPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]
        if preference_values[1] > preference_values[2]:
            secondaryPreference = preference[1]
    if page_num == 0 and topPreference:
        if secondaryPreference:
            condition = {"$or": [{"class": topPreference}, {"class": secondaryPreference}]}
            total_news = list(news_collection.find(condition).sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
            sliced_news = total_news[begin_index: end_index]
        else:
            total_news = list(news_collection.find({"class": topPreference}).sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
            sliced_news = total_news[begin_index: end_index]
        total_news_digest = [x['digest'] for x in total_news[begin_index: end_index]]
        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

    else:
        try:
            news_digests = pickle.loads(redis_client.get(user_id))
        except:
            news_digests = []
        if news_digests:
            total_news = list(news_collection.find({'digest': {'$nin': news_digests}}).sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        else:
            total_news = list(news_collection.find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        # total_news_digest = [x['digest'] for x in total_news]

        # redis_client.set(user_id, pickle.dumps(total_news_digest))
        # redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index: end_index]
        # if redis_client.get(user_id) is not None:
        #     news_digests = pickle.loads(redis_client.get(user_id))
        #     sliced_news_digest = news_digests[begin_index:end_index]
        #     sliced_news = list(news_collection.find({'digest': {'$in': sliced_news_digest}}))
        # else:
        #     total_news = list(news_collection.find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        #     total_news_digest = [x['digest'] for x in total_news]
        #
        #     redis_client.set(user_id, pickle.dumps(total_news_digest))
        #     redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        #     sliced_news = total_news[begin_index: end_index]


    for news in sliced_news:
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
        if 'class' in news and news['class'] == topPreference:
            news['reason'] = 'Recommend'
        if 'class' in news and news['class'] == secondaryPreference:
            news['reason2'] = 'Recommend'
    return json.loads(dumps(sliced_news))


def logNewsClickForUser(user_id, news_id):
    Logger.info('Click log for {0} at {1}'.format(user_id, news_id))
    amqp_client = AMQPClient(queue_name=LOG_CLICKS_TASK_QUEUE_NAME, callBack=None)
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}
    click_log_collection = Mongo().get_collection(CLICK_LOGS_TABLE_NAME)
    click_log_collection.insert_one(message)
    message['timestamp'] = str(message['timestamp'])
    message.pop('_id')
    amqp_client.sendMessage(message)
    return {"success": True}


def searchNews(keyword, page_num):
    key = str(keyword) + "#"
    page_num = int(page_num)
    begin_index = (page_num) * NEWS_LIST_BATCH_SIZE
    end_index = (page_num + 1) * NEWS_LIST_BATCH_SIZE
    news_collection = Mongo().get_collection(name=NEWS_TABLE_NAME)

    if redis_client.get(key) is not None:
        news_digests = pickle.loads(redis_client.get(key))
        sliced_news_digests = news_digests[begin_index:end_index]
        Logger.info(sliced_news_digests)
        sliced_news = list(news_collection.find({'digest':{'$in':sliced_news_digests}}))
    else:
        search = '.*' + keyword + '.*'
        condition = {
            "$or": [
                {'title': {'$regex': re.compile(search)}},
                {'description': {'$regex': re.compile(search)}}
            ]
        }
        total_news = list(
            news_collection.find(condition).sort([('publishedAt', -1)])
            .limit(NEWS_LIMIT)
        )

        total_news_digest = [x['digest'] for x in total_news]
        redis_client.set(key, pickle.dumps(total_news_digest))
        redis_client.expire(key, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index:end_index]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))

