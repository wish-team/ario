import os
import sys
from werkzeug.middleware.shared_data import SharedDataMiddleware
from wsgiref.simple_server import make_server

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


#
# app = SharedDataMiddleware(Application(control), {
#     '/static': os.path.join(os.path.dirname(__file__), 'templates/static')
# })


@control.route(method=['GET'], route="/static")
def static_files():
    print("STATIC_FILES")


def create_app(with_static=True):
    app = Application(control)
    if with_static:
        print("XXX")
        app = SharedDataMiddleware(app, {
            '/static': os.path.join(os.path.dirname(__file__), 'templates/static')
        })
    return app


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
    run = make_server('', 5000, app)
    print('Demo server started http://localhost:5000')
    run.serve_forever()

# ario = Ario()
# ario.run()
