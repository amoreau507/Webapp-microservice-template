from libs.logger import logger
from libs.queue.ServerQueueServiceImpl import ServerQueueServiceImpl

logging = logger.create_logger('src', force_to_recreate=True)


def hello_word(body):
    logging.info("hello word request received")
    return "%s" % body


queue = ServerQueueServiceImpl('username', 'password', 'localhost', 5672, 'hello_word', hello_word)

if __name__ == "__main__":
    logging.debug("Test start")
