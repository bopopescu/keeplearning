#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : hotqueue.py
# Author    : wuqingfeng@

import logging
import time
from multiprocessing import Process

logger = logging.getLogger('process_test_log')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('/tmp/process_test.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def run():
    for i in range(100):
        logger.info("test is %s", i)
        time.sleep(1)


if __name__ == '__main__':

    p1 = Process(target=run, args=tuple())
    is_alive = p1.is_alive()
    logger.info("is_alive: %s", is_alive)
    p1.start()
    is_alive = p1.is_alive()
    logger.info("is_alive: %s", is_alive)
    logger.info("main test end!")
