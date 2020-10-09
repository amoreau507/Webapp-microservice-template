from os.path import isfile
from os import mkdir

import sys
import logging
import pika
import uuid

# create the log file if it doesn't exist
if not isfile('logs'):
    try:
        mkdir('logs')
    except OSError:
        print("Creation of the directory logs failed")
    else:
        print("Successfully created the directory logs ")
if not isfile('logs/test.log'):
    with open('logs/test.log', "w") as l:
        l.write('test Logs\n')

logging.basicConfig(filename='logs/test.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


class Test(object):
    def __init__(self):
        self.credentials = pika.PlainCredentials('username', 'password')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', self.credentials)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='hello_word', durable=True)
        self.channel.basic_qos(prefetch_size=0)
        self.channel.basic_consume(queue='hello_word', on_message_callback=self.hello_word)
        self.channel.start_consuming()

    def hello_word(self, ch, method, props, body):
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=str("hello word %s" % str(uuid.uuid4()))
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    logging.debug("Test start")
    rcpServer = Test()
