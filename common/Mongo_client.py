import logging
from pymongo import MongoClient, database

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

MONGO_DB_HOST = "localhost"
MONGO_DB_PORT = 27017
DB_NAME = "tap-news"


class Mongo(object):

    def __init__(self):
        self.client = MongoClient(MONGO_DB_HOST, MONGO_DB_HOST)

    def get_db(self, db_name) -> database.Database:
        return self.client.get_database(db_name)



