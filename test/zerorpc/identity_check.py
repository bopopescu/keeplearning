#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : identity_check.py
# Author    : wuqingfeng@

import zmq
import zhelpers


if __name__ == '__main__':
    context = zmq.Context()
    sink = context.socket(zmq.ROUTER)
    sink.bind("inproc://example")

    anonymous = context.socket(zmq.DEALER)
    anonymous.connect("inproc://example")
    anonymous.send_multipart([b"", b"ROUTER use a generated 5 byte identity"])
    zhelpers.dump(sink)

    identified = context.socket(zmq.DEALER)
    identified.setsockopt(zmq.IDENTITY, b'PEER2')
    identified.connect("inproc://example")
    identified.send_multipart([b"", b"ROUTE socket use REQ's socket identity"])
    zhelpers.dump(sink)
