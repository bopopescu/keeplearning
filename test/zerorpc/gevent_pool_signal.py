#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : gevent_pool_signal.py
# Author    : wuqingfeng@

from gevent import sleep
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore

class SocketPool(object):

    def __init__(self):
        self.pool = Pool(1000)
        self.pool.start()

    def listen(self, socket):
        while True:
            socket.recv()

    def add_handler(self, socket):
        if self.pool.full():
            raise Exception("At maximum pool size")
        else:
            self.pool.spawn(self.listen, socket)

    def shutdown(self):
        self.pool.kill()


sem = BoundedSemaphore(10)


def worker1(n):
    sem.acquire()
    print('Worker %i acquired semaphore' % n)
    sleep(0)
    sem.release()
    print('Worker %i release semaphore' % n)


def worker2(n):
    with sem:
        print('Worker %i acquired semaphore' % n)
        sleep(0)
    print('Worker %i release semaphore' % n)


if __name__ == '__main__':
    pool = Pool()
    pool.map(worker1, xrange(0, 2))
    pool.map(worker2, xrange(3, 6))