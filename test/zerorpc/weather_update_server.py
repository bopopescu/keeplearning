#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : weather_update_server.py
# Author    : wuqingfeng@

import zmq
import time
from random import randrange


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://0.0.0.0:5556")

    while True:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)
        print "start to publish someting..."
        socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
        print "finish to publish(%i %i %i)" % (zipcode, temperature, relhumidity)
        time.sleep(5)