import uuid

from services.commun import logger
from services.commun.queue import ServerQueueServiceImpl

logging = logger.create_logger('impl', force_to_recreate=True)


def hello_word(body):
    logging.info("hello word request received")
    return "hello word %s" % str(uuid.uuid4())


queue = ServerQueueServiceImpl('username', 'password', 'localhost', 5672, 'hello_word', hello_word)

if __name__ == "__main__":
    logging.debug("Test start")
