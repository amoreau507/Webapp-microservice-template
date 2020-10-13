from os.path import isfile, isdir
from os import mkdir, remove

import logging

LOG_FOLDER = '../logs'


def create_logger(module_name, level=logging.INFO, force_to_recreate=False):
    path = LOG_FOLDER + "/" + module_name + '.log'
    logger = logging.getLogger(module_name)

    # create file handler which logs even debug messages
    if force_to_recreate and isfile(path):
        remove(path)

    if not isdir(LOG_FOLDER):
        try:
            mkdir(LOG_FOLDER)
        except OSError:
            print("Creation of the directory logs failed")
        else:
            print("Successfully created the directory logs ")
    if not isfile(path):
        open(path, "a").close()

    logging.basicConfig(filename=path, level=level, format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')
    return logger
