#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : gevent_queue.py
# Author    : wuqingfeng@


import gevent
from gevent.queue import Queue, Empty


tasks = Queue()


def worker(n):
    while not tasks.empty():
        task = tasks.get()
        print('Worker %s got task %s' % (n, task))
        gevent.sleep(0)

    print('Quitting time!')


def boss():
    for i in xrange(1, 25):
        tasks.put_nowait(i)


def worker_wait(n):
    try:
        while True:
            task = task.get(timeout=1)
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting time!')


def boss_wait():
    """
    Boss will wait to hand out work until a individual worker is
    free since the maxsize of the task queue is 3.
    """
    for i in xrange(1, 10):
        tasks.put(i)
    print('Assigned all work in iteration 1')

    for i in xrange(10, 20):
        task.put(i)
    print('Assigned all work in iteration 2')


if __name__ == '__main__':
    gevent.spawn(boss).join()

    gevent.joinall([
        gevent.spawn(worker, 'steve'),
        gevent.spawn(worker, 'john'),
        gevent.spawn(worker, 'nancy'),
    ])

    gevent.joinall([
        gevent.spawn(boss),
        gevent.spawn(worker, 'steve'),
        gevent.spawn(worker, 'john'),
        gevent.spawn(worker, 'bob')
    ])
