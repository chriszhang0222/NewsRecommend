import os
import sys
import logging
import json
from common.utils.news_classes import classes
from common.AMQP_client import AMQPClient
from common.Mongo_client import Mongo

logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)


NUM_OF_CLASSES = len(classes)

INITIAL_P = 1.0 / NUM_OF_CLASSES

ALPHA = 0.1

LOG_CLICKS_TASK_QUEUE_NAME = "LOG_CLICKS_TASK_QUEUE"
PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        Logger.error('msg:{} error'.format(msg))
        return
    if ('userId' not in msg
    or 'newsId' not in msg
    or 'timestamp' not in msg):
        Logger.error('msg:{} error'.format(msg))
        return
    userId = msg['userId']
    newsId = msg['newsId']

    model = Mongo.get_collection(name=PREFERENCE_MODEL_TABLE_NAME).find_one({'userId': userId})
    if model is None:
        Logger.info('Create preference model for new user:{0}'.format(userId))
        new_model = {'userId': userId}
        perference = {}
        for i in classes:
            perference[i] = float(INITIAL_P)
        new_model['preference'] = perference
        model = new_model
    Logger.info('Updating preference model from new user:{}'.format(userId))
    news = Mongo.get_collection().find_one({'digest': newsId})
    if (news is None
    or 'class' not in news):
        Logger.info('News:{} skipping'.format(news))


    click_class = news['class']
    old_p = model['preference'][click_class]

    model['preference'][click_class] = float((1-ALPHA)*old_p + ALPHA)

    for i, prob in model['preference'].items():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])
    Logger.info('Preference Model: {}'.format(model))
    Mongo.get_collection(name=PREFERENCE_MODEL_TABLE_NAME).replace_one({'userId': userId}, model, upsert=True)


rabbit_client = AMQPClient(LOG_CLICKS_TASK_QUEUE_NAME, handle_message)
rabbit_client.receiveMessage()