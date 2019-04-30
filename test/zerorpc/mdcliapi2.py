#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : mdcliapi2.py
# Author    : wuqingfeng@

import sys
import logging
import zmq
import MDP
from zhelpers import dump


class MajorDomoClient(object):
    broker = None
    ctx = None
    client = None
    poller = None
    timeout = 2500
    verbose = False

    def __init__(self, broker, verbose=False):
        self.broker = broker
        self.verbose = verbose
        self.ctx = zmq.Context()
        self.poller = zmq.Poller()
        logging.basicConfig(format="%(asctime)s %(message)s", 
                            datefmt="%Y-%m-%d %H:%M:%S",
                            level=logging.INFO)
        self.reconnect_to_broker()

    def reconnect_to_broker(self):
        if self.client:
            self.poller.unregister(self.client)
            self.client.close()
        self.client = self.ctx.socket(zmq.DEALER)
        self.client.linger = 0
        self.client.connect(self.broker)
        self.poller.register(self.client, zmq.POLLIN)
        if self.verbose:
            logging.info("I: connecting to broker at %s...", self.broker)

    def send(self, service, request):
        if not isinstance(request, list):
            request = [request]

        # Prefix request with protocol frames
        # Frame 0: empty (REQ emulation)
        # Frame 1: "MDPCxy" (six bytes, MDP/Client x.y)
        # Frame 2: Service name (printable string)
        
        request = ['', MDP.C_CLIENT, service] + request
        if self.verbose:
            logging.warn("I: send request to '%s' service: ", service)
            dump(request)
        self.client.send_multipart(request)

    def recv(self):
        try:
            items = self.poller.poll(self.timeout)
        except KeyboardInterrupt:
            return

        if items:
            msg = self.client.recv_multipart()
            if self.verbose:
                logging.info("I: received reply:")
                dump(msg)

            assert len(msg) >= 4

            empty = msg.pop(0)
            header = msg.pop(0)
            assert MDP.C_CLIENT == header

            service = msg.pop(0)
            return msg
        else:
            logging.warn("W: permanent error, abandoning request")


def main():
    verbose = '-v' in sys.argv
    client = MajorDomoClient("tcp://127.0.0.1:5555", verbose)
    requests = 100000
    for i in xrange(requests):
        request = "Hello world"
        try:
            client.send("echo", request)
        except KeyboardInterrupt:
            print "send interrupted, aborting"
            return
    count = 0
    while count < requests:
        try:
            reply = client.recv()
        except KeyboardInterrupt:
            break
        else:
            if reply is None:
                break
        count += 1
    print "%i requests/replies processed" % count


if __name__ == '__main__':
    main()