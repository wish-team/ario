import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ario import RouterController, Endpoint, Application, json, html, setup_jinja, jinja, redirect
from ario.status import forbidden 

setup_jinja("./templates")

control = RouterController(debug=True)

@control.route(method=["GET", "PUT", "INSERT"], route="/user")
class UserEndpoint(Endpoint):
    @html
    def get(request, response):
        body = '''
        <title>user</title>
        <h1>Hello World</h1>
        '''
        response.cookie("key", "value", {"path": "/user"})
        response.start()
        return body

    @redirect("https://github.com/")
    def insert(request, response):
        pass


@control.route(method=["GET", "POST", "HEAD"], route="/")
class DashboardEndpoint(Endpoint):
    @json
    def get(request, response):
        data = {
            "name": "shayan",
            "family_name": "shafaghi",
            "age": 21,
            "phonenumber": "09197304252"
        }
        response.start()
        return data


    def head(request, response):
        status = '200 OK'
        data = b'damn'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ]
        response(status, response_headers)
        return data


@control.route(method=["GET", "POST"], route="/user/profile")
class DashboardEndpoint(Endpoint):
    @html
    def get(request, response):
        body = '''
            <title>profile</title>
            <body>
            <h1>This is user profile</h1>
            </body>
        '''
        response.start()
        return body


@control.route(method=["GET", "POST"], route="/user/$id")
class DashboardEndpoint(Endpoint):
    @jinja("base.html")
    def get(request, response, id):
        params = {"my_string": id, "my_list": [0, 1, 2]}
        response.start()
        return params


@control.route(method=["GET", "POST"], route="/user/profile")
class DashboardEndpoint(Endpoint):
    @html
    def get(request, response):
        body = '''
            <title>profile</title>
            <body>
            <h1>This is user profile</h1>
            </body>
        '''
        response.start()
        return body


@control.route(method=['GET'], route="/bug")
class bug(Endpoint):
    def get(request, response):
        raise Exception("This is an exception")
        return b"302 Moved Temporarily"


@control.route(method=['GET'], route="/foo")
class RedirectEndpoint(Endpoint):
    def get(request, response):
        response.temp_redirect("/")
        return b"302 Moved Temporarily"


@control.default()
@html
def not_found(request, response):
    body = '''
    <title>Not Found</title>
    <body>
    <h1>404 Not Found</h1>
    </body>
    '''
    response.status = forbidden()
    response.start()
    return body


app = Application(control)
