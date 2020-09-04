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


class RouteNode:
    def __init__(self, method, path, handler=None, childs=[]):
        self.method = method
        self.path = path
        self.handler = handler
        self.childs = childs




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


    def make_route_tree(self, route, method, cls):
        route = route.replace("/", "", 1)
        tokens = route.split("/")
        routes = self.routes['childs']
        for i in range(len(tokens)):
            if len(routes) == 0:
                if len(tokens) - 1 == i:
                    new_route = {
                            "path": tokens[i],
                            "method": method,
                            "handler": cls(method, route),
                            "childs": []
                        }
                else:
                    new_route = {
                            "path": tokens[i],
                            "method": [],
                            "handler": None,
                            "childs": []
                        }
                routes.append(new_route)
                routes = new_route['childs']
                continue
            for (j, r) in enumerate(routes):    
                if r["path"] != tokens[i]:
                    if j == len(routes) - 1:
                        if len(tokens) - 1 == i:
                            new_route = {
                                    "path": tokens[i],
                                    "method": method,
                                    "handler": cls(method, route),
                                    "childs": []
                                }
                        else:
                            new_route = {
                                    "path": tokens[i],
                                    "method": [],
                                    "handler": None,
                                    "childs": []
                                }
                    routes.append(new_route)
                    routes = new_route['childs']
                    continue 
                if len(tokens) - 1 == i:
                    r['method'] = method 
                    r['handler'] = cls(method, route) 
                else:
                    routes = r["childs"]
                break


    def route(self, method, route):
        def wrapper(cls):
            self.make_route_tree(route, method, cls)
            print(self.routes)
        return wrapper
