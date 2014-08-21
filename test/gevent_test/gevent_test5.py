import gevent
from gevent.event import AsyncResult
from gevent.queue import Queue, Empty

# a = AsyncResult()

# def setter():
#     gevent.sleep(3)
#     a.set('Hello!')

# def waiter():
#     print a.get()

# gevent.joinall([
#     gevent.spawn(setter),
#     gevent.spawn(waiter)
# ])

# tasks = Queue()

# def worker(n):
#     while not tasks.empty():
#         task = tasks.get()
#         print 'Worker %s got task %s' % (n, task)
#         gevent.sleep(0)

#     print 'Quitting time!'

# def boss():
#     for i in xrange(1 ,25):
#         tasks.put_nowait(i)

# gevent.spawn(boss).join()

# gevent.joinall([
#     gevent.spawn(worker, 'steve'),
#     gevent.spawn(worker, 'john'),
#     gevent.spawn(worker, 'nancy')
# ])

tasks = QUeue(maxsize=3)

def worker(n):
    try:
        while True:
            task = tasks.get(timeout=1)
            print 'Worker %s got task %s' % (n, task)
            gevent.sleep(0)
    except Empty:
        print 'Quitting time!'

def boss():
    for i in xrange(1, 10):
        tasks.put(i)
    print 'Assigned all work in iteration 1'

    for i in xrange(10, 20):
        tasks.put(i)
    print 'Assigned all work in iteration 2'


gevent.joinall([
    gevent.spawn(boss),
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'john'),
    gevent.spawn(worker, 'bob')
])