import os


class Environment:
    def __init__(self):
        self.db_hostname = os.environ.get('DB_HOSTNAME', 'localhost')
        self.db_username = os.environ.get('DB_USERNAME', 'admin')
        self.db_password = os.environ.get('DB_PASSWORD', 'admin')
        self.db_port = int(os.environ.get('DB_PORT', '27017'))
        self.db_name = os.environ.get('DB_NAME', 'mongo')
