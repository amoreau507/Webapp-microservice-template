from flask import Flask
from flask_cors import CORS
from services.common.queue import ClientQueueServiceImpl
from services.common import logger

logging = logger.create_logger('impl', force_to_recreate=True)

app = Flask(__name__)
cors = CORS(app)

hello_word_mq = ClientQueueServiceImpl('username', 'password', 'localhost', 5672, 'hello_word')


@app.route('/', methods=['GET'])
def index():
    return hello_word_mq.get_response()


if __name__ == "__main__":
    logging.info("Gateway start")
    app.run(host='0.0.0.0', debug=True, ssl_context=('../conf/cert.pem', '../conf/key.pem'))
