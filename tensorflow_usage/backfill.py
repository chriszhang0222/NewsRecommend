import logging
from backend.client.news_topic_client import classify
from common.Mongo_client import Mongo

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

if __name__ == '__main__':
    cursor = Mongo.get_collection(name='news').find({})
    count = 0
    for news in cursor:
        count += 1
        Logger.info(count)
        if 'class' not in news:
            Logger.info('Popolating classess...')
            description = news['description']
            if description is None:
                description = news['title']
            if description:
                topic = classify(description)
                news['class'] = topic
                Mongo.get_collection(name='news').replace_one({'digest': news['digest']}, news, upsert=True)


