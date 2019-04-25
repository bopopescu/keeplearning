#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : cluster_prototype_flow.py
# Author    : wuqingfeng@


import random
import sys
import threading
import time

import zmq

try:
    raw_input
except NameError:
    raw_input = input

NBR_CLIENTS = 10
NBR_WORKERS = 3


def tprint(msg):
    sys.stdout.write(msg + '\n')

def client_task(name, i):
    """Request-reply client using REQ socket"""
    ctx = zmq.Context()
    client = ctx.socket(zmq.REQ)
    client.identity = (u"Client-%s-%s" % (name, i)).encode('ascii')
    client.connect("ipc://%s-localfe.ipc" % name)
    while True:
        client.send(b"HELLO")
        try:
            reply = client.recv()
        except zmq.ZMQError:
            return
        tprint("Client-%s: %s" % (i, reply))
        time.sleep(1)


def worker_task(name, i):
    """Worker using REQ socket to do LRU routing"""
    ctx = zmq.Context()
    worker = ctx.socket(zmq.REQ)
    worker.identity = (u"Worker-%s-%s" % (name, i)).encode("ascii")
    worker.connect("ipc://%s-localbe.ipc" % name)

    worker.send(b"READY")

    while True:
        try:
            msg = worker.recv_multipart()
        except zmq.ZMQError:
            return
        tprint("Worker-%s: %s\n" % (i, msg))
        msg[-1] = b"OK"
        worker.send_multipart(msg)

def main(myself, peers):
    print("I: preparing broker at %s..." % myself)

    ctx = zmq.Context()

    cloudfe = ctx.socket(zmq.ROUTER)
    if not isinstance(myself, bytes):
        ident = myself.encode('ascii')
    else:
        ident = myself

    cloudfe.identity = ident
    cloudfe.bind("ipc://%s-cloud.ipc" % myself)

    cloudbe = ctx.socket(zmq.ROUTER)
    cloudbe.identity = ident
    for peer in peers:
        tprint("I: connecting to cloud frontend at %s" % peer)
        cloudbe.connect("ipc://%s-cloud.ipc" % peer)
    
    if not isinstance(peer[0], bytes):
        peers = [peer.encode("ascii") for peer in peers]

    localfe = ctx.socket(zmq.ROUTER)
    localfe.bind("ipc://%s-localfe.ipc" % myself)
    localbe = ctx.socket(zmq.ROUTER)
    localbe.bind("ipc://%s-localbe.ipc" % myself)

    raw_input("Press Enter when all brokers are started: ")

    for i in range(NBR_WORKERS):
        thread = threading.Thread(target=worker_task, args=(myself, i))
        thread.daemon = True
        thread.start()

    for i in range(NBR_CLIENTS):
        thread_c = threading.Thread(target=client_task, args=(myself, i))
        thread_c.daemon = True
        thread_c.start()

    # Interesting part
    # -------------------------------------------------------------
    # Request-reply flow
    # - Poll backends and process local/cloud replies
    # - While worker available, route localfe to local or cloud
    
    workers = []

    pollerbe = zmq.Poller()
    pollerbe.register(localbe, zmq.POLLIN)
    pollerbe.register(cloudbe, zmq.POLLIN)

    pollerfe = zmq.Poller()
    pollerfe.register(localfe, zmq.POLLIN)
    pollerfe.register(cloudfe, zmq.POLLIN)

    while True:
        try:
            events = dict(pollerbe.poll(1000 if workers else None))
        except zmq.ZMQError:
            break

        msg = None
        if localbe in events:
            msg = localbe.recv_multipart()
            address, empty, msg = msg[:2], msg[2:]
            workers.append(address)

            if msg[-1] = b'READY':
                msg = None
        elif cloudbe in events:
            msg = cloudbe.recv_multipart()
            address, empty, msg = msg[:2], msg[2:]

        if msg in not None:
            address = msg[0]
            if address in peers:
                cloudfe.send_multipart(msg)
            else:
                localfe.send_multipart(msg)

        while workers:
            events = dict(pollerfe.poll(0))
            reroutable = False
            if cloudfe in events:
                msg = cloudfe.recv_multipart()
                reroutable = False
            elif localfe in events:
                msg = localfe.recv_multipart()
                reroutable = True
            else:
                break

            if reroutable and peers and random.randint(0, 4) == 0:
                msg = [random.choice(peers), b''] + msg
                cloudbe.send_multipart(msg)
            else:
                msg = [worker.pop(), b''] + msg
                localbe.send_multipart(msg)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(myself=sys.argv[1], peers=sys.argv[2:])
    else:
        print("Usage: cluster_prototype_flow.py <myself> <peer_1> <peer_2> ... <peer_N>")
        sys.exit(1)