#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : psenvsub.py
# Author    : wuqingfeng@


import zmq


def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:5563")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"B")

    while True:
        [address, contents] = subscriber.recv_multipart()
        print("[%s] %s" % (address, contents))

    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()