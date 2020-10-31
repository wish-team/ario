import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from werkzeug.serving import run_simple
from werkzeug.middleware.shared_data import SharedDataMiddleware

from ario import RouterController, Endpoint, Application, json, html, setup_jinja, jinja, redirect
from ario.status import forbidden, ok
from ario.static import serve_static
from ario.exceptions import UnauthorizedError

setup_jinja("./templates")

control = RouterController(debug=True, langs=['fa', 'en'])

def handler(message):
    return b"Unauthorized error from handler"
UnauthorizedError.handler = handler

@control.route(method=["GET", "PUT", "INSERT"], route="/user")
class UserEndpoint(Endpoint):
    @html
    def get(request, response):
        if not request.lang:
            print("No lang is set")
        else:
            print("responsig from /", request.lang, "/user")
        body = '''
        <title>user</title>
        <h1>Hello World</h1>
        '''
        print(request.URI)
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
        print("REQ: ", request.file)
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


@control.route(method=["GET", "POST"], route="/user_all/*id")
class DashboardEndpoint(Endpoint):
    @json
    def get(request, response, id):
        print(id)
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


@control.route(method=['GET', 'POST'], route="/bug")
class bug(Endpoint):
    def get(request, response):
        raise Exception("This is an exception")
        return b"302 Moved Temporarily"

    def post(request, response):
        raise UnauthorizedError


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


@control.route(method=['POST', 'GET'], route='/file')
class PostFile(Endpoint):
    def post(request, response):
        form = request.body
        fileitem = form['userfile']
        filename = fileitem.filename.replace('\\','/').split('/')[-1].strip()
        with open(filename, 'wb') as f:
            while True:
                data = fileitem.file.read(1024)
                if not data:
                    break
                f.write(data)
        print('name: ', form['fname'].value)
        print('last name: ', form['lname'].value)
        print('None', form.getvalue('lnam'))
        return "hello"

    def get(request, response):
        file = serve_static("<path-to-file>", response)
        return file



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
