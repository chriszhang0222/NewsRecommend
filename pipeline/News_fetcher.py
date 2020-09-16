import os
import sys
import json
import logging
from newspaper import Article
from common.AMQP_client import AMQPClient
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

DEDUPE_NEWS_TASK_QUEUE_NAME = "top-new-DEDUPE_NEWS_TASK_QUEUE_NAME"
SCRAPE_NEWS_TASK_QUEUE_NAME = "top-news-SCRAPE_NEWS_TASK_QUEUE"

dedupe_news_queue_client = AMQPClient(queue_name=DEDUPE_NEWS_TASK_QUEUE_NAME)


def scrape_message_call_back(message):
    if message is not None:
        if isinstance(message, str):
            message = json.loads(message)
        try:
            if message is None or not isinstance(message, dict):
                Logger.error('Message is broken')
                return
            task = message
            text = None
            article = Article(task['url'])
            article.download()
            article.parse()
            task['text'] = article.text
            Logger.info(task)
            dedupe_news_queue_client.sendMessage(json.dumps(message))
        except Exception as e:
            Logger.error(e)
            return


scrape_news_queue_client = AMQPClient(queue_name=SCRAPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client.receiveMessage()