import json
import logging
from common.Mongo_client import Mongo
import backend.operations as operations

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

SERVER_HOST = 'localhost'
SERVER_PORT = 4040


def add(num1, num2):
    Logger.info('calling add with {}:{}'.format(num1, num2))
    return num1 + num2


def get_one_news():
    Logger.info('Get One news called')
    return operations.getOneNews()


def get_news_summaries_for_user(user_id, page_num):
    Logger.info('Get news summaryies for {0} at {1}'.format(user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)


def search_news(keyword, page_num):
    Logger.info('Search News called with {}'.format(keyword))
    return operations.searchNews(keyword, page_num)

def log_news_click(user_id, news_id):
    Logger.info('Log News Click for:{0} with {1}'.format(user_id, news_id))
    return operations.logNewsClickForUser(user_id, news_id)


rpc_server = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
rpc_server.register_function(search_news, 'searchNews')
rpc_server.register_function(get_one_news, 'getOneNews')
rpc_server.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
rpc_server.register_function(log_news_click, 'logNewsClickForUser')


Logger.info('Start RPC Server at {}:{}'.format(SERVER_HOST, SERVER_PORT))
rpc_server.serve_forever()