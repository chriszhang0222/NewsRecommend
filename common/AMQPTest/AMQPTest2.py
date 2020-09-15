from common.AMQP_client import AMQPClient

import json
client = AMQPClient('test')
client.sendMessage(json.dumps({'ok': 'yes'}))