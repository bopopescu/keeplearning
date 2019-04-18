#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : hello_world_server_zmq.py
# Author    : wuqingfeng@

import time
import zmq


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://0.0.0.0:5555")
    # socket.connect("tcp://127.0.0.1:5560")

    while True:
        message = socket.recv()
        print("Received request: %s" % message)

        # time.sleep(1)

        socket.send(b"World")