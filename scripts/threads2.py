import concurrent.futures
import logging
import threading
import time


def thread_example(index):
    logging.info(f"Thread {index} starting")
    time.sleep(index + 10)
    logging.info(f"Thread {index} finishing")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_example, range(3))
