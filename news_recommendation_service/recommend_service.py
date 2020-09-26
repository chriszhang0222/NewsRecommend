import operator
import os
import sys
import logging
import json
from common.utils.news_classes import classes
from common.AMQP_client import AMQPClient
from common.Mongo_client import Mongo
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)


PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def getPreferenceForUser(user_id):

    model = Mongo.get_collection(PREFERENCE_MODEL_TABLE_NAME).find_one({'user_id': user_id})
    if model is None:
        return []
    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []
    return sorted_list


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')

Logger.info("Starting Recommend Service server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
