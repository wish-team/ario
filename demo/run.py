import os
import sys
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
PACKAGE_PARENT = '..'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from ario import RouterController, Endpoint, Application, jinja, setup_jinja, Ario

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


class Render(object):
    def dispatch_request(self, request):
        return Response('Hello World!')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


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


if __name__ == '__main__':
    app = Application(control)
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

# ario = Ario()
# ario.run()
