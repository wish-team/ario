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
        data = b'Hello, World!\n'
        status = '200 OK'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ]
        response(status, response_headers)
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


@control.route(method=["GET", "POST"], route="/dashboard/baz")
class DashboardEndpoint(Endpoint):
    pass


@control.route(method=["GET", "POST"], route="/user/test")
class DashboardEndpoint(Endpoint):
    pass

app = Application(control)
