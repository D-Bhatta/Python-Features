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

    threads = []
    for index in range(5):
        logging.info(f"Main  : create and start thread {index}")
        new_thread = threading.Thread(target=thread_example, args=(index,))
        threads.append(new_thread)
        new_thread.start()

    for index, thread in enumerate(threads):
        logging.info(f"Main  : before joining thread {index}")
        thread.join()
        logging.info(f"Main  : finishing thread {index}")
