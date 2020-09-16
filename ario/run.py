from gunicorn import sock
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


app = SharedDataMiddleware(app, {
    '/static': os.path.join(os.path.dirname(__file__), 'static')
})

# ario = Ario()
# ario.run()
