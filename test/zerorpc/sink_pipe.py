#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : sink_pipe.py
# Author    : wuqingfeng@

import sys
import time
import zmq


if __name__ == '__main__':

    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://0.0.0.0:5558")

    s = receiver.recv()
    sys.stdout.write("%s"%s)
    tstart = time.time()

    for task_nbr in range(100):
        s = receiver.recv()
        sys.stdout.write("%s"%s)
        if task_nbr % 10 == 0:
            sys.stdout.write(":")
        else:
            sys.stdout.write(".")
        sys.stdout.flush()

    tend = time.time()
    print("Total elapsed time: %d msec" % ((tend-tstart)*1000) )