#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : request_reply_broker.py
# Author    : wuqingfeng@

import zmq


def message_queue():
    context = zmq.Context()

    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://0.0.0.0:5559")

    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://0.0.0.0:5560")

    zmq.proxy(frontend, backend)

    frontend.close()
    backend.close()
    context.term()


if __name__ == '__main__':

    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend.bind("tcp://0.0.0.0:5559")
    backend.bind("tcp://0.0.0.0:5560")

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())

        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv_multipart()
            backend.send_multipart(message)

        if socks.get(backend) == zmq.POLLIN:
            message = backend.recv_multipart()
            frontend.send_multipart(message)