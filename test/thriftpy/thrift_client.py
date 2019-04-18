#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : thrift_client.py
# Author    : wuqingfeng@

import thriftpy2
from thriftpy2.rpc import make_client


if __name__ == '__main__':
    time_thrift = thriftpy2.load("time_service.thrift", module_name="time_thrift")
    client = make_client(time_thrift.TimeService, '127.0.0.1', 6000)

    print(client.get_time())
