#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : hello_world_server.py
# Author    : wuqingfeng@

import gevent
import zerorpc
import time
import multiprocessing

class HelloRPC(object):

    def __init__(self, pid):
        print "init pid: %s" % pid
        self.pid = pid

    def hello(self, name):
        print self.pid
        hellorpc = "Hello, %s" % name
        # time.sleep(30)
        return hellorpc

    def hello2(self, name):
        print self.pid
        hellorpc = "Hello, %s" % name
        gevent.sleep(11)
        return hellorpc

    def hello3(self, name):
        print self.pid
        hellorpc = "Hello, %s" % name
        gevent.sleep(31)
        return hellorpc

def server_main(uri, pid):
    # s = zerorpc.Server(HelloRPC(pid))
    # s.bind(uri)
    # s.run()
    s = zerorpc.Puller(HelloRPC(pid))
    s.bind(uri)
    s.run()

if __name__ == '__main__':

    p1 = multiprocessing.Process(target=server_main, args=("tcp://0.0.0.0:4242", 1))
    p2 = multiprocessing.Process(target=server_main, args=("tcp://0.0.0.0:4243", 2))

    for p in [p1, p2]:
        p.start()
    # server_main("tcp://0.0.0.0:4242")
    # s = zerorpc.Server(HelloRPC())
    # s.bind("tcp://0.0.0.0:4242")
    # s.run()