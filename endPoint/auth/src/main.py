import jwt
import uuid

from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from libs.db.environment import Environment
from libs.db.exceptions import DuplicateException
from libs.db.mongo import Mongo
from libs.queue.ClientQueueServiceImpl import ClientQueueServiceImpl
from libs.logger import logger

logging = logger.create_logger('src', force_to_recreate=True)

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'acme'
app.config['CORS_HEADERS'] = ['Content-Type']

env_config = Environment()
db = Mongo(
    env_config.db_hostname,
    port=env_config.db_port,
    username=env_config.db_username,
    password=env_config.db_password,
    dbname=env_config.db_name)

hello_word_mq = ClientQueueServiceImpl('username', 'password', 'localhost', 5672, 'hello_word')


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.environ['HTTP_AUTHORIZATION'][2:-1]

        if not token:
            return make_response('could not verify', 401, {'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.get_user_by_email(data['email'])
        except:
            return make_response('Invalid authentication', 409, {'message': 'token is invalid'})

        return func(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET'])
@login_required
def index():
    return hello_word_mq.get_response(body=str(uuid.uuid4()))


@app.route('/login', methods=['GET', 'POST'])
@cross_origin()
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = db.get_user_by_email(auth.username)
    user_agent = request.headers["user-agent"]

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({"user-agent": user_agent, 'public_id': user.public_id, 'email': user.email, 'isAdmin': user.isAdmin, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])

        resp = jsonify({'token': str(token)})
        resp.status_code = 200
        return resp

    return make_response('Bad password', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    try:
        db.insert_user(data['email'], data['first_name'], data['first_name'], hashed_password, isAdmin=False)
    except DuplicateException as err:
        return jsonify({'message': str(err)}), 400

    new_user = db.get_user_by_email(data['email'])
    logging.info("New user: %s" % new_user.to_json())

    return jsonify({'message': ("New user: %s" % new_user.to_json())})


if __name__ == "__main__":
    logging.info("Gateway start")
    db.connect()
    app.run(host='0.0.0.0', debug=True, ssl_context=('../conf/cert.pem', '../conf/key.pem'))
