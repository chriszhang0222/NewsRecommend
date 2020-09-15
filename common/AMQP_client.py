import pika
import logging
import json
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)


class AMQPClient(object):

    def __init__(self, queue_name, callBack=None):
        # auth = pika.PlainCredentials('root', 'root')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='127.0.0.1',
            port=5672,
            socket_timeout=3
        ))
        self.callBack = callBack
        self.queue_name = queue_name
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        Logger.info('Connect to RabbitMQ:{}-{}'.format('127.0.0.1', '5672'))

    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=message)
        Logger.info('Message send to {}:{}'.format(self.queue_name, message))

    def messageCallBack(self, ch, method, properties, body):
        if self.callBack is not None:
            self.callBack(body)
        Logger.info('Receive message: {}'.format(body))


    def receiveMessage(self):
        self.channel.basic_consume(on_message_callback=self.messageCallBack,
                                   queue=self.queue_name,
                                   auto_ack=True)
        try:
            self.channel.start_consuming()
        except Exception:
            self.channel.stop_consuming()
