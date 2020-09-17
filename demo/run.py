from ario.application import Application
from ario.router import RouterController, Endpoint
from ario.jinja import jinja
import os
from werkzeug.middleware.shared_data import SharedDataMiddleware


class Ario:
    def __init__(self):
        self.instance_path = False

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        """
        :param host: the location that listen on
        :param port: the port that the app will be serve
        :param debug:
        :param load_dotenv:
        :param options:
        :return:
        """
        _host = "127.0.0.1"
        _port = 5000
        host = host or _host
        port = int(_port)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_reloader=True, **options)


control = RouterController(debug=True)


@control.route(method=["GET", "POST"], route="/user/$id")
class DashboardEndpoint(Endpoint):
    @jinja("base.html")
    def get(request, response, id):
        params = {"my_string": id, "my_list": [0, 1, 2]}
        response.start()
        return params


app = SharedDataMiddleware(Application(control), {
    '/static': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
    print("Hello")

# ario = Ario()
# ario.run()
