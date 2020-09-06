import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ario import RouterController, Endpoint, Application

control = RouterController()

@control.route(method=["GET", "PUT", "INSERT"], route="/user")
class UserEndpoint(Endpoint):
    def get(request, response):
        data = b'''
        <title>user</title>
        <h1>Hello World</h1>
        '''
        status = '200 OK'
        response.content_type = "text/html"
        return data


    def insert(request, response):
        print("here")
        data = b'Hello, World!\n'
        status = '200 OK'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ]
        response(status, response_headers)
        return data


@control.route(method=["GET", "POST", "HEAD"], route="/")
class DashboardEndpoint(Endpoint):
    def get(request , response):
        data = b'This is Route\n'
        status = '200 OK'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ]
        response(status, response_headers)
        return data


    def head(request , response):
        status = '200 OK'
        data =  b'damn'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ]
        response(status, response_headers)
        return data


@control.route(method=["GET", "POST"], route="/user/test")
class DashboardEndpoint(Endpoint):
    pass


@control.route(default=True)
def not_found(request, response): 
    data = b'400 Not Found\n'
    status = '404 Not Found'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    response(status, response_headers)
    return data

app = Application(control)
