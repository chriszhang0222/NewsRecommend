import logging
import jsonrpclib

logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

URL = "http://localhost:5050/"

client = jsonrpclib.Server(URL)


def getPreferenceForUser(userId):
    preference = client.getPreferenceForUser(userId)
    Logger.info('Preference List: {}'.format(preference))
    return preference