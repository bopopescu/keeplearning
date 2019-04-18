#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : thrift_server.py
# Author    : wuqingfeng@

import time
import thriftpy2
from thriftpy2.rpc import make_server


class Dispatcher(object):
    def get_time(self):
        return str(time.ctime())


if __name__ == '__main__':

    time_thrift = thriftpy2.load("time_service.thrift", module_name="time_thrift")

    server = make_server(time_thrift.TimeService, Dispatcher(), '127.0.0.1', 6000)
    server.serve()