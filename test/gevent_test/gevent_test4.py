import time
import gevent
from gevent import select

start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)

def gr1():
    print 'gr1 Started Polling:', tic()
    select.select([], [], [], 2)
    print 'gr1 Ended Polling:', tic()

def gr2():
    print 'gr2 Started Polling:', tic()
    select.select([], [], [], 2)
    print 'gr2 Ended Polling:', tic()

def gr3():
    print 'Hey lets do some stuff while the greenlets poll, at', tic()
    gevent.sleep(1)
    print 'gr3 Ended'

gevent.joinall([
    gevent.spawn(gr1),
    gevent.spawn(gr2),
    gevent.spawn(gr3),
])