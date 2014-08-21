import gevent
from gevent import Greenlet

def foo(message, n):
    print n
    gevent.sleep(n)
    print message

thread1 = Greenlet.spawn(foo, 'Hello', 2)

thread2 = gevent.spawn(foo, 'I live!', 1)

thread3 = gevent.spawn(lambda x: (x+1), 2)

threads = [thread1, thread2, thread3]

gevent.joinall(threads)