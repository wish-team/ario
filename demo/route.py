import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from werkzeug.serving import run_simple
from werkzeug.middleware.shared_data import SharedDataMiddleware

from ario import RouterController, Endpoint, Application, json, html, setup_jinja, jinja, redirect
from ario.status import forbidden, ok

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
        return body


@control.route(method=["GET", "POST"], route="/user/$id")
class DashboardEndpoint(Endpoint):
    @jinja("base.html")
    def get(request, response, id):
        params = {"my_string": id, "my_list": [0, 1, 2]}
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
        return body


@control.route(method=['GET'], route="/bug")
class bug(Endpoint):
    def get(request, response):
        raise Exception("This is an exception")
        return b"302 Moved Temporarily"


@control.route(method=['GET', 'INSERT'], route="/foo")
class RedirectEndpoint(Endpoint):
    def get(request, response):
        response.temp_redirect("/")
        return b"302 Moved Temporarily"

    @json
    def insert(request, response):
        response.status = ok()
        body = request.body
        return body


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
    return body


# app = Application(control)

if __name__ == '__main__':
    app = Application(control)
    app = SharedDataMiddleware(app, {
        '/static': os.path.join(os.path.dirname(__file__), 'templates/static')
    })
    print('Demo server started http://localhost:5000')
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
