import logging
import jsonrpclib

logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)
URL = "http://localhost:6060"

client = jsonrpclib.Server(URL)

def classify(text):
    topic = client.classify(text)
    Logger.info('Topic: {}'.format(topic))
    return topic
