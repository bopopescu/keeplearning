#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : apscheduler.py
# Author    : wuqingfeng@

import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler


def run_test():
    print "I am running now..."
    time.sleep(10)
    print "I am end now!"

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = BlockingScheduler()
    scheduler.configure(logger=logging)
    scheduler.add_job(func=run_test, args=(), trigger='interval', jobstore='default',
                      replace_existing=True, seconds=20)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
