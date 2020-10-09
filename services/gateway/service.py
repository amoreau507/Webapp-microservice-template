from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from os.path import isfile
from os import mkdir
import pika
import uuid
import sys
import logging

# create the log file if it doesn't exist
if not isfile('logs'):
    try:
        mkdir('logs')
    except OSError:
        print("Creation of the directory logs failed")
    else:
        print("Successfully created the directory logs ")
if not isfile('logs/gateway.log'):
    with open('logs/gateway.log', "w") as l:
        l.write('gateway Logs\n')

logging.basicConfig(filename='logs/gateway.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

app = Flask(__name__)
cors = CORS(app)


class ClientQueue(object):
    def __init__(self):
        self.credentials = pika.PlainCredentials('username', 'password')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', self.credentials)
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', durable=True, exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.coor_id == props.correlation_id:
            self.response = body

    def get_response(self):
        self.response = None
        self.coor_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='hello_word',
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.coor_id),
            body=''
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response


rpcClient = ClientQueue()


@app.route('/', methods=['GET'])
def index():
    return rpcClient.get_response()


if __name__ == "__main__":
    logging.debug("Gateway start")
    app.run(host='0.0.0.0', debug=True, ssl_context=('conf/cert.pem', 'conf/key.pem'))
