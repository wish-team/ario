import os
import sys
from werkzeug.middleware.shared_data import SharedDataMiddleware
from wsgiref.simple_server import make_server
from werkzeug.serving import run_simple

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
PACKAGE_PARENT = '..'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from ario import RouterController, Endpoint, Application, jinja, setup_jinja, html
from ario.status import forbidden


control = RouterController(debug=True)
setup_jinja("./templates")


@control.route(method=["GET", "POST"], route="/user/$id")
class DashboardEndpoint(Endpoint):
    @jinja("base.html")
    def get(request, response, id):
        params = {"my_string": id, "my_list": [0, 1, 2]}
        response.start()
        return params


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


if __name__ == '__main__':
    app = Application(control)
    app = SharedDataMiddleware(app, {
        '/static': os.path.join(os.path.dirname(__file__), 'templates/static')
    })
    print('Demo server started http://localhost:5000')
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
