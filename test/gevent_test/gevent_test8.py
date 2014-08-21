import gevent
from gevent.queue import Queue, Empty
from gevent.pywsgi import WSGIServer
import json

data_source = Queue()
def producer():
    count = 1
    while True:
        if count%2 :
            data_source.put_nowait("Hello World %s" % count)
        else:
            data_source.put_nowait("I'm a coder %s!" % count)
        gevent.sleep(60*10)
        count += 1

def ajax_endpoint(environ, start_response):
    # print environ
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json')
    ]
    try:
        datum = data_source.get(timeout=60*10)
    except Empty:
        datum = []

    start_response(status, headers)
    return json.dumps(datum)

gevent.spawn(producer)

WSGIServer(('', 8000), ajax_endpoint).serve_forever()
