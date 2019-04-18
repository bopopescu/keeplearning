#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : syncsub.py
# Author    : wuqingfeng@

import time
import zmq


def main():
    context = zmq.Context()

    subscriber = context.socket(zmq.SUB)
    subscriber.connect('tcp://127.0.0.1:5561')
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    time.sleep(1)

    syncclient = context.socket(zmq.REQ)
    syncclient.connect('tcp://127.0.0.1:5562')

    syncclient.send(b'')

    syncclient.recv()

    nbr = 0

    while True:
        msg = subscriber.recv()
        if msg == b'END':
            break
        nbr += 1

    print("Received %d updates" % nbr)


if __name__ == '__main__':
    main()

