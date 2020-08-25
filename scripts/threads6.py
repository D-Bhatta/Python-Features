import concurrent.futures
import logging
import queue
import random
import threading
import time

SENTINEL = object()


def producer(pipeline, event):
    """
    Pretend we are getting a msg
    """
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info(f"Producer got message: {message}")
        pipeline.set_message(message, "Producer")
    logging.info("Producer received EXIT event. Exiting....")


def consumer(pipeline, event):
    """
    Pretend we are saving a msg
    """
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info(
                f"Consumer storing message: {message} (queue size = {pipeline.qsize()}"
            )
    logging.info("Consumer received EXIT event. Exiting....")


class Pipeline(queue.Queue):
    """
    Class to allow a single element pipeline between producer and consumer
    """

    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug(f"{name}: about to get from queue")
        value = self.get()
        logging.debug(f"{name}: got value {value}")
        return value

    def set_message(self, value, name):
        logging.debug(f"{name}: about to add {value} to queue")
        self.put(value)
        logging.debug(f"{name}: {value} added to queue")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.INFO)
    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()
