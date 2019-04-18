#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : worker_pipe.py
# Author    : wuqingfeng@

import sys
import time
import zmq


if __name__ == '__main__':

    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://127.0.0.1:5557")

    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://127.0.0.1:5558")
    num = 1
    while True:
        s = receiver.recv()
        # print "workload: %s" % s
        sys.stdout.write('.')
        sys.stdout.flush()

        time.sleep(int(s)*0.001)

        sender.send(b'%d'%num)
        # time.sleep(5)
        num += 1