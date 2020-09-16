import json
import logging
from common.Mongo_client import Mongo
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

SERVER_HOST = 'localhost'
SERVER_PORT = 4040


def add(num1, num2):
    Logger.info('calling add with {}:{}'.format(num1, num2))
    return num1 + num2


rpc_server = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
rpc_server.register_function(add, 'add')

Logger.info('Start RPC Server at {}:{}'.format(SERVER_HOST, SERVER_PORT))
rpc_server.serve_forever()