from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://hfihunhv:6M6k7M224aJRdbBUmcNykK7XWdTmgmgI@otter.rmq.cloudamqp.com/hfihunhv"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
    sentMsg = {'test': 'demo'}
    client.sendMessage(sentMsg)
    client.sleep(1)
    receiveMsg = client.getMessage()

if __name__ == "__main__":
    test_basic()