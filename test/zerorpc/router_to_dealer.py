#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : router_to_dealer.py
# Author    : wuqingfeng@

import time
import random
import zmq
from threading import Thread


def worker_a(context=None):
    context = context or zmq.Context()
    worker = context.socket(zmq.DEALER)
    worker.setsockopt(zmq.IDENTITY, b'A')
    worker.connect("ipc://routing.ipc")

    total = 0

    while True:
        request = worker.recv()
        finished = request == b"END"
        if finished:
            print "A received: %s" % total
            break
        total += 1


def worker_b(context=None):
    context = context or zmq.Context()
    worker = context.socket(zmq.DEALER)
    worker.setsockopt(zmq.IDENTITY, b'B')
    worker.connect("ipc://routing.ipc")

    total = 0

    while True:
        request = worker.recv()
        finished = request == b"END"
        if finished:
            print "B received: %s" % total
            break
        total += 1


if __name__ == '__main__':
    context = zmq.Context()
    server = context.socket(zmq.ROUTER)
    server.bind("ipc://routing.ipc")
    Thread(target=worker_a).start()
    Thread(target=worker_b).start()
    time.sleep(1)

    for _ in range(10):
        ident = random.choice([b'A', b'A', b'B'])
        workload = b"This is the workload"
        server.send_multipart([ident, workload])

    server.send_multipart([b'A', b'END'])
    server.send_multipart([b'B', b'END'])
