#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : gevent_actor.py
# Author    : wuqingfeng@

import gevent
from gevent.queue import Queue


class Actor(gevent.Greenlet):

    def __init__(self):
        self.inbox = Queue()
        super(Actor, self).__init__()

    def receive(self, message):
        raise NotImplemented()

    def _run(self):
        self.running = True

        while self.running:
            message = self.inbox.get()
            print "message: %s" % message
            self.receive(message)


class Pinger(Actor):
    def receive(self, message):
        print(message)
        pong.inbox.put('ping')
        gevent.sleep(0)

class Ponger(Actor):
    def receive(self, message):
        print(message)
        ping.inbox.put('pong')
        gevent.sleep(0)

ping = Pinger()
pong = Ponger()

if __name__ == '__main__':
    ping.start()
    pong.start()
    ping.inbox.put('start-1')
    # pong.inbox.put('start-2')
    gevent.joinall([ping, pong])
    # print "bbbb"