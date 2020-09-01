

class Application:
    def __init__(self, controller=None):
        self.routes = []
        if controller in not None:
            self.controller= None

    def __call__(self, environ, start_response):
        response = self.controller(environ)
