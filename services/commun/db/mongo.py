import uuid

from pymongo import MongoClient
from datetime import datetime
from services.commun import logger
from services.commun.db import exceptions

logging = logger.create_logger('db', force_to_recreate=True)


class Mongo:
    grid_side_length = 5

    def __init__(self, url, port=27017, username='', password='', dbname='default'):
        self._client = None
        self._db = None
        self._dbname = dbname
        self._url = url
        self._port = port
        self._username = username
        self._password = password

    def connect(self):
        self._client = MongoClient(f'mongodb://{self._username}:{self._password}@{self._url}', port=self._port)
        self._db = self._client[self._dbname]
        logging.info('successfully logged in to database.')

    def disconnect(self):
        self._client.close()
        self._client = None
        self._db = None

    def insert_user(self, email, first_name, last_name, pwd_hash, isAdmin=False):
        user = User(email, first_name, last_name, pwd_hash, isAdmin)
        if self.get_user_by_email(email) is not None:
            raise exceptions.DuplicateException("Email already use.")

        self._db['users'].insert_one(user.to_json())

    def get_user_by_email(self, email):
        user = self._db['users'].find_one({'email': email})
        if user is not None:
            return User(
                user['email'],
                user['first_name'],
                user['last_name'],
                user['password'],
                isAdmin=user['isAdmin'],
                last_passwords=user['last_passwords'],
                creation_date=user['creation_date'],
                last_activity=user['last_activity'],
                public_id=user['public_id']
            )
        else:
            return None

    def info(self):
        return self._client.server_info()

    def is_up(self):
        return True if self._client else False


class User(object):
    def __init__(self, email, first_name, last_name, pwd_hash, isAdmin=False, last_passwords: list = [], creation_date=datetime.utcnow(), last_activity=None, public_id=str(uuid.uuid4())):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = pwd_hash
        self.last_passwords = last_passwords
        self.isAdmin = isAdmin
        self.creation_date = creation_date
        self.last_activity = last_activity
        self.public_id = public_id

    def to_json(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'last_passwords': self.last_passwords,
            'isAdmin': self.isAdmin,
            'creation_date': self.creation_date,
            'last_activity': self.last_activity,
            'public_id': self.public_id
        }
