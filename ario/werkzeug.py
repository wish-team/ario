from werkzeug.serving import run_simple


class Ario:
    def __init__(self):
        self.host = None

    def run(self):
        _host = "127.0.0.1"
        _port = 5000
        host = _host
        port = int(_port)
        run_simple(host, port, self, use_reloader=True)
