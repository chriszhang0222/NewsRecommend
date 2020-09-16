from common.AMQP_client import AMQPClient
DEDUPE_NEWS_TASK_QUEUE_NAME = "top-new-DEDUPE_NEWS_TASK_QUEUE_NAME"
SCRAPE_NEWS_TASK_QUEUE_NAME = "top-news-SCRAPE_NEWS_TASK_QUEUE"


def clearQueue(queue_name):
    amqp_client = AMQPClient(queue_name)
    number_of_message = 0
    while True:
        if amqp_client is not None:
            msg = amqp_client.get_message()
            if msg is not None:
                return
