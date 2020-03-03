import logging
import threading
import time


def lock_holder(lock):
    logging.debug('Iniciando')
    while True:
        lock.acquire()
        try:
            logging.debug('El lector  1 esta ocupando la BD')
            time.sleep(5)
        finally:
            logging.debug('El lector 1 ha dejado de usar la BD')
            lock.release()
        time.sleep(5)


def worker(lock):
    logging.debug('Iniciando')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Lector 2 intentando acceder')
        have_it = lock.acquire(0)
        try:
            num_tries += 1
            if have_it:
                logging.debug('Intento %d: Lector 2 accedio',num_tries)
                num_acquires += 1
            else:
                logging.debug('Intento %d: No accedio',num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Realizado después de %d intentos', num_tries)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

lock = threading.Lock()

holder = threading.Thread(target=lock_holder,args=(lock,), name='Lector 1', daemon=True,)
holder.start()

worker = threading.Thread(target=worker, args=(lock,), name='Lector 2',)
worker.start()
