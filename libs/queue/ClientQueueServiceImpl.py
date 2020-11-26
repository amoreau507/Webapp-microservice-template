import pika
import uuid

ENCODING = "utf-8"


class ClientQueueServiceImpl(object):
    def __init__(self, username, password, host, port, queue_keys):
        self.queue_keys = queue_keys
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port, '/', self.credentials)
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', durable=True, exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = ''
        self.coor_id = ''

    def on_response(self, ch, method, props, body):
        if self.coor_id == props.correlation_id:
            self.response = body

    def get_response(self, body=''):
        self.response = None
        self.coor_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_keys,
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.coor_id),
            body=body,
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response
