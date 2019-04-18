#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : mspoller.py
# Author    : wuqingfeng@

import zmq


if __name__ == '__main__':

    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://127.0.0.1:5557")

    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.01:5556")
    subscriber.setsockopt(zmq.SUBSCRIBE, b'10001')

    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    poller.register(subscriber, zmq.POLLIN)

    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break

        if receiver in socks:
            message = receiver.recv()

        if subscriber in socks:
            message = subscriber.recv()

