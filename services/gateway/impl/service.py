import jwt
import uuid

from flask import Flask, g, request, redirect, url_for, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS
from datetime import datetime, timedelta
from services.commun.db.exceptions import *
from services.commun.db.environment import Environment
from services.commun.db.mongo import Mongo
from services.commun.queue import ClientQueueServiceImpl
from services.commun import logger

logging = logger.create_logger('impl', force_to_recreate=True)

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'acme'
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
        token = None

        if 'WEB_APP_TOKEN' in request.cookies:
            token = request.cookies['WEB_APP_TOKEN']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.get_user_by_email(data['email'])
        except:
            return jsonify({'message': 'token is invalid'})

        return func(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['GET'])
@login_required
def index():
    return hello_word_mq.get_response(body=str(uuid.uuid4()))


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


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = db.get_user_by_email(auth.username)
    user_agent = request.headers["user-agent"]

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"user-agent": user_agent, 'public_id': user.public_id, 'email': user.email, 'isAdmin': user.isAdmin, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])

        resp = make_response(jsonify({'message': "Login successful"}), 200)
        resp.set_cookie('WEB_APP_TOKEN', token)
        return resp

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


if __name__ == "__main__":
    logging.info("Gateway start")
    db.connect()
    app.run(host='0.0.0.0', debug=True, ssl_context=('../conf/cert.pem', '../conf/key.pem'))
