import gevent
from gevent import Greenlet

# class MyGreenlet(Greenlet):

#     def __init__(self, message, n):
#         Greenlet.__init__(self)
#         self.message = message
#         self.n = n

#     def _run(self):
#         print self.message
#         gevent.sleep(self.n)


# g = MyGreenlet("Hi there!", 3)
# g.start()
# g.join()

def win():
    return 'You win!'

def fail():
    raise Exception('You fail at failing.')

winner = gevent.spawn(win)
loser = gevent.spawn(fail)

print winner.started
print loser.started

try:
    gevent.joinall([winner, loser])
except Exception as e:
    print 'This will never be reached'

print winner.value
print loser.value

print winner.ready()
print loser.ready()

print winner.successful()
print loser.successful()

print loser.exception