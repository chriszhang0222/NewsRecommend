import pika
import json


class CloudAMQPClient:
    def __init__(self, url, queue_name):
        self.cloud_amqp_url = url
        self.queue_name = queue_name
        self.params = pika.URLParameters(url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def sendMessage(self, message):
        """
        send a message
        :param message:
        :return:
        """
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print("Sent message to %s: %s" % (self.queue_name, message))

    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame is not None:
            print("Received message from %s: %s" % (self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print("No message returned")
            return None

    def sleep(self, seconds):
        self.connection.sleep(seconds)