#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : psenvpub.py
# Author    : wuqingfeng@


import time
import zmq


def main():

    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://0.0.0.0:5563")

    while True:
        publisher.send_multipart([b"A", b"We don't want to see this"])
        publisher.send_multipart([b"B", b"We would like to see this"])
        time.sleep(1)

    publisher.close()
    context.term()


if __name__ == "__main__":
    main()