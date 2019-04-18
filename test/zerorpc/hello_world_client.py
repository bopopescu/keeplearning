#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : hello_world_client.py
# Author    : wuqingfeng@

import zerorpc

if __name__ == '__main__':
    # c = zerorpc.Client(passive_heartbeat=True)
    c = zerorpc.Pusher()
    c.connect(["tcp://127.0.0.1:4242", "tcp://127.0.0.1:4243"])
    # c.connect("tcp://127.0.0.1:4242")
    result = c.hello("RPC")
    print result
    # result = c.hello2("RPC", timeout=20, async=False)
    result = c.hello2("RPC")
    print result
    # print type(result), result
    # result = c.hello("RPC")
    # result = c.hello2("RPC", timeout=20, async=False)
