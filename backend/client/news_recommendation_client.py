import logging
import jsonrpclib
import operator
from common.Mongo_client import Mongo

logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

URL = "http://localhost:5050/"

client = jsonrpclib.Server(URL)

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def getPreferenceForUserRPC(userId):
    preference = client.getPreferenceForUser(userId)
    Logger.info('Preference List: {}'.format(preference))
    return preference


def getPreferenceForUser(user_id):
    model = Mongo().get_collection(PREFERENCE_MODEL_TABLE_NAME).find_one({'userId': user_id})
    if model is None:
        return [], []
    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return [], []
    return sorted_list, sorted_value_list