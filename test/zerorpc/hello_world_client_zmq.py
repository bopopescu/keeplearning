#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : hello_world_client_zmq.py
# Author    : wuqingfeng@

import zmq


if __name__ == '__main__':
    context = zmq.Context()

    print("Connecting to hello world server...")

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")
    # socket.connect("tcp://127.0.0.1:5559")

    for request in range(10):
        print("Sending request %s ..." % request)
        socket.send(b"Hello")

        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))