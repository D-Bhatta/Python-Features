import concurrent.futures
import logging
import random
import threading
import time

SENTINEL = object()


def producer(pipeline):
    """
    Pretend we are getting a msg
    """
    for index in range(10):
        message = random.randint(1, 101)
        logging.info(f"Producer got message: {message}")
        pipeline.set_message(message, "Producer")

    pipeline.set_message(SENTINEL, "Producer")


def consumer(pipeline):
    """
    Pretend we are saving a msg
    """
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info(f"Consumer storing message: {message}")


class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer
    """

    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        logging.debug(f"{name}: about to acquire getlock")
        self.consumer_lock.acquire()
        logging.debug(f"{name}: have getlock")
        message = self.message
        logging.debug(f"{name}: getting message {message}")
        logging.debug(f"{name}: about to release setlock")
        self.producer_lock.release()
        logging.debug(f"{name}: released setlock")
        return message

    def set_message(self, message, name):
        logging.debug(f"{name}: about to acquire setlock")
        self.producer_lock.acquire()
        logging.debug(f"{name}: have setlock")
        logging.debug(f"{name}: setting message {message}")
        self.message = message
        logging.debug(f"{name}: about to release getlock")
        self.consumer_lock.release()
        logging.debug(f"{name}: released getlock")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.INFO)
    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
