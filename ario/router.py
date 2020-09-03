from dataclasses import dataclass
from typing import List
from ario.request import Request


@dataclass
class Endpoint:
    method: List[str]
    route: str


    def __call__(self):
        print(f"{self.route} called with {self.method}")


    def __eq__(self, other):
        if (self.method == other.method 
                and self.route == other.route):
            return True
        else:
            return False


class RouterController:
    __instance = None


    @staticmethod
    def get_instance():
        if RouterController.__instance is None:
            RouterController()
        return RouterController.__instance


    def __init__(self):
        if RouterController.__instance is None:
            self.routes = {
                    "path": "/",
                    "method": [],
                    "handler": None,
                    "childs": []
                }
            RouterController.__instance = self
        else:
            raise Exception("Controller already instantiated")


    def __call__(self, environ, start_response):
        req = Request(environ)
        method  = req.method
        path = req.path


    def route(self, method, route):
        def wrapper(cls):
            print(route)
            route = route.replace("/", "", 1)
            tokens = route.split("/")
            routes = self.routes
            for i in range(len(tokens)):
                if routes["path"] != tokens[i]:
                    continue 
                if len(tokens) - 1 == i:
                    new_route = {
                        "path": tokens[i],
                        "method": [method],
                        "handler": cls(method, route),
                        "childs": []
                    }
                    routes['childs'].append(new_route)
                    break
                else:
                    routes = routes["childs"]
            print(routes)
        return wrapper


