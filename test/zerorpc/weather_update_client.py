#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : weather_update_client.py
# Author    : wuqingfeng@

import sys
import zmq


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from weather server...")
    socket.connect("tcp://127.0.0.1:5556")

    zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"

    if isinstance(zip_filter, bytes):
        zip_filter = zip_filter.decode('ascii')
    socket.setsockopt_string(zmq.SUBSCRIBE, u'')
    message = socket.recv_string()
    zipcode, temperature, relhumidity = message.split()
    print zipcode, temperature, relhumidity

    # socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

    # total_temp = 0
    # for update_nbr in range(5):
    #     message = socket.recv_string()
    #     zipcode, temperature, relhumidity = message.split()
    #     total_temp += int(temperature)

    # print "Average temperature for zipcode '%s' was %dF" % (
    #     zip_filter, total_temp / (update_nbr+1)
    # )