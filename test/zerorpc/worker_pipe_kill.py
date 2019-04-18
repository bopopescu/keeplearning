#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : worker_pipe_kill.py
# Author    : wuqingfeng@

import sys
import time
import zmq


if __name__ == '__main__':
    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://127.0.0.1:5557")

    controller = context.socket(zmq.SUB)
    controller.connect("tcp://127.0.0.1:5559")
    controller.setsockopt(zmq.SUBSCRIBE, b"")

    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://127.0.0.1:5558")

    poller = zmq.Poller()
    poller.register(receiver, zmq.POLLIN)
    poller.register(controller, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())

        if socks.get(receiver) == zmq.POLLIN:
            message = receiver.recv_string()
            workload = int(message)
            time.sleep(workload / 1000.0)
            sender.send_string(message)

            sys.stdout.write(".")
            sys.stdout.flush()

        if socks.get(controller) == zmq.POLLIN:
            break

    receiver.close()
    sender.close()
    controller.close()
    context.term()