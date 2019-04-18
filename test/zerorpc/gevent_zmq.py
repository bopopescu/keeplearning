#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : gevent_zmq.py
# Author    : wuqingfeng@


import gevent
from gevent_zeromq import zmq


def server(context):
    server_socket = context.socket(zmq.REQ)
    server_socket.bind("tcp://127.0.0.1:5000")

    for request in range(1, 10):
        server_socket.send(b"Hello")
        print('Switched to Server for %s' % request)
        server_socket.recv()


def client():
    client_socket = context.socket(zmq.REP)
    client_socket.connect("tcp://127.0.0.1:5000")

    for request in range(1, 10):
        client_socket.recv()
        print('Switched to Client for %s' % request)
        client_socket.send("World")


if __name__ == '__main__':
    context = zmq.Context()
    reply = gevent.spawn(server)
    request = gevent.spawn(client)

    gevent.joinall([reply, request])
