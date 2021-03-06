#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : load_balancing_zloop.py
# Author    : wuqingfeng@


from __future__ import print_function
import threading
import time
import zmq

from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

NBR_CLIENTS = 10
NBR_WORKERS = 3


def worker_thread(worker_url, i):
    """ Worker using REQ socket to do LRU routing """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    socket.identity = (u"Worker-%d" % i).encode('ascii')
    socket.connect(worker_url)

    socket.send(b"READY")

    try:
        while True:
            address, empty, request = socket.recv_multipart()
            print("%s: %s\n" % (socket.identity.decode('ascii'),
                                request.decode('ascii')), end='')
            socket.send_multipart([address, b'', b'OK'])
    except zmq.ContextTerminated:
        # context terminated so quit silently
        return


def client_thread(client_url, i):
    """ Basic request-reply client using REQ socket """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.identity = (u"Client-%d" % i).encode('ascii')
    socket.connect(client_url)
    socket.send(b"HELLO")
    reply = socket.recv()
    # print(reply)
    print("%s: %s\n" % (socket.identity.decode('ascii'),
                        reply.decode('ascii')), end='')


class LRUQueue(object):
    """LRUQueue class using ZMQStream/IOLoop for event dispatching"""
    def __init__(self, backend_socket, frontend_socket):
        self.available_workers = 0
        self.workers = []
        self.client_nbr = NBR_CLIENTS

        self.backend = ZMQStream(backend_socket)
        self.frontend = ZMQStream(frontend_socket)
        self.backend.on_recv(self.handle_backend)

        self.loop = IOLoop.instance()

    def handle_backend(self, msg):
        # Queue worker address for LRU routing
        worker_addr, empty, client_addr = msg[:3]

        assert self.available_workers < NBR_WORKERS

        self.available_workers += 1
        self.workers.append(worker_addr)

        assert empty == b""

        if client_addr != b"READY":
            empty, reply = msg[3:]

            assert empty == b""
            self.frontend.send_multipart([client_addr, b'', reply])
            self.client_nbr -= 1
            if self.client_nbr == 0:
                self.loop.add_timeout(time.time() + 1, self.loop.stop)

        if self.available_workers == 1:
            self.frontend.on_recv(self.handle_frontend)

    def handle_frontend(self, msg):
        client_addr, empty, request = msg
        assert empty == b""

        self.available_workers -= 1
        worker_id = self.workers.pop()

        self.backend.send_multipart([worker_id, b'', client_addr, b'', request])

        if self.available_workers == 0:
            self.frontend.stop_on_recv()


def main():
    """main method"""
    url_worker = "ipc://backend.ipc"
    url_client = "ipc://frontend.ipc"

    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind(url_client)
    backend = context.socket(zmq.ROUTER)
    backend.bind(url_worker)

    for i in range(NBR_WORKERS):
        thread = threading.Thread(target=worker_thread, args=(url_worker, i))
        thread.daemon = True
        thread.start()

    for i in range(NBR_CLIENTS):
        thread_c = threading.Thread(target=client_thread, args=(url_client, i))
        thread_c.daemon = True
        thread_c.start()

    queue = LRUQueue(backend, frontend)

    queue.loop.start()


if __name__ == '__main__':
    main()