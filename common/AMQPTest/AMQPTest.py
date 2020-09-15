from common.AMQP_client import AMQPClient


def callBack(message):
    print(len(message))

consumer = AMQPClient('test', callBack)

consumer.receiveMessage()
