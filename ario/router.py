from dataclasses import dataclass
from typing import List
from ario.request import Request
import pdb


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
            nonlocal route
            route = route.replace("/", "", 1)
            tokens = route.split("/")
            tokens.insert(0, "/")
            routes = self.routes
            routes = [routes]
            for i in range(len(tokens)):
                if len(routes) == 0:
                    new_route = {
                            "path": tokens[i],
                            "method": [method],
                            "handler": cls(method, route),
                            "childs": []
                        }
                    routes.append(new_route)
                    if len(tokens) - 1 == i:
                        break
                for r in routes:    
                    if r["path"] != tokens[i]:
                        continue 
                    if len(tokens) - 1 == i:
                        new_route = {
                            "path": tokens[i],
                            "method": [method],
                            "handler": cls(method, route),
                            "childs": []
                        }
                        r['childs'].append(new_route)
                    else:
                        routes = r["childs"]
                    break
            print(self.routes)
        return wrapper


