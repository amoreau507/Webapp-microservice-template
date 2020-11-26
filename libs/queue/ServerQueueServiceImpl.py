import pika

ENCODING = "utf-8"


class ServerQueueServiceImpl(object):
    def __init__(self, username, password, host, port, queue_keys, callback):
        self.callback = callback
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host, port, '/', self.credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_keys, durable=True)
        self.channel.basic_qos(prefetch_size=0)
        self.channel.basic_consume(queue=queue_keys, on_message_callback=self.default_callback)
        self.channel.start_consuming()

    def default_callback(self, ch, method, props, body):
        response = self.callback(body.decode(ENCODING))
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=str(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
