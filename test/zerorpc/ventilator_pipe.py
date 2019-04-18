#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : ventilator.py
# Author    : wuqingfeng@

import sys
import zmq
import random
import time

try:
    raw_input
except NameError:
    raw_input = input


if __name__ == "__main__":

    context = zmq.Context()
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://0.0.0.0:5557")

    sink = context.socket(zmq.PUSH)
    sink.connect("tcp://127.0.0.1:5558")

    print("Press Enter when the workers are ready: ")
    _ = raw_input()
    print("Sending tasks to workers...")

    sink.send(b'0')

    random.seed()
    total_msec = 0
    for task_nbr in range(100):

        workload = random.randint(1, 100)
        total_msec += workload
        sys.stdout.write("workload: %s "%workload)
        sys.stdout.flush()
        sender.send_string(u"%i" % workload)
        # time.sleep(10)

    print("Total expected cost: %s msec" % total_msec)

    time.sleep(1)
