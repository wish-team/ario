import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ario import Application, RouterController, Endpoint, Request 

def controller(environ, start_response):
    """Simplest possible application object"""
    req = Request(environ)
    length = req.content_length
    print('length: ', length)
    met = req.method
    print('method: ',met)
    path = req.path
    print('path: ',path)
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])


app = Application(controller)
