#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : router_to_req.py
# Author    : wuqingfeng@

import time
import random
from threading import Thread

import zmq
import zhelpers


NBR_WORKERS = 10

#LRU
def worker_thread(context=None):
    context = context or zmq.Context()
    worker = context.socket(zmq.REQ)

    zhelpers.set_id(worker)
    worker.connect("tcp://127.0.0.1:5671")

    total = 0
    while True:
        worker.send(b"ready")
        workload = worker.recv()
        finished = workload == b"END"
        if finished:
            print("Process: %d tasks" % total)
            break
        total += 1

        time.sleep(0.1 * random.random())


if __name__ == '__main__':
    context = zmq.Context()
    server = context.socket(zmq.ROUTER)
    server.bind("tcp://0.0.0.0:5671")

    for _ in range(NBR_WORKERS):
        Thread(target=worker_thread).start()

    for _ in range(NBR_WORKERS * 10):
        address, empty, ready = server.recv_multipart()
        # print "address is reach: %s" % address
        server.send_multipart([
            address,
            b'',
            b'This is the workload',
        ])

    for _ in range(NBR_WORKERS):
        address, empty, ready = server.recv_multipart()
        server.send_multipart([
            address,
            b'',
            b'END'
        ])