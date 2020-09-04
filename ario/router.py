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


class RouteNode:
    def __init__(self, method, path, handler=None, childs=[]):
        self.method = method
        self.path = path
        self.handler = handler
        self.childs = childs


    def add_node(self, route, method, handler):
        tokens = RouteNode.__tokenize_route(route)
        routes = self.childs
        for i in range(len(tokens)):
            if len(routes) == 0:
                if isinstance(handler, Endpoint):
                    handler = handler(method, route)
                if len(tokens) - 1 == i:
                    node = RouteNode(method, tokens[i], handler, [])
                else:
                    node = RouteNode([], tokens[i], [], [])
                routes.append(node)
                routes = node.childs
                continue
            for (j, r) in enumerate(routes):
                if r.path != tokens[i]:
                    if j == len(routes) - 1:
                        if len(tokens) - 1 == i:
                            node = RouteNode(method, tokens[i], handler, [])
                        else:
                            node = RouteNode([], tokens[i], [], [])
                    routes.append(node)
                    routes = node.childs
                    continue
                if len(tokens) - 1 == i:
                    r.method = method
                    if isinstance(handler, Endpoint):
                        handler = handler(method, route)
                    r.handdler = handler
                else:
                    routes = r.childs
                break


    def find_node(self, route):
        tokens = RouteNode.__tokenize_route(route)
        if route == self.path:
            return (self.handler, self.method)
        routes = self.childs
        for i in range(len(tokens)):
            match_flag = False
            for (j, r) in enumerate(routes):
                if r.path != tokens[i]:
                    continue
                match_flag = True
                if len(tokens) - 1 == i:
                    return (r.handler, r.method)
                else:
                    routes = r.childs
                break
            if not match_flag:
                return None, None


    @staticmethod
    def __tokenize_route(route):
        route = route.replace("/", "", 1)
        tokens = route.split("/")
        return tokens


    def __repr__(self):
        return f"path: {self.path}, methods: {self.method}, \n childs: {self.childs} \n"


class RouterController:
    __instance = None


    @staticmethod
    def get_instance():
        if RouterController.__instance is None:
            RouterController()
        return RouterController.__instance


    def __init__(self):
        if RouterController.__instance is None:
            self.routes = RouteNode([], "/", None)
            RouterController.__instance = self
        else:
            raise Exception("Controller already instantiated")


    def __call__(self, environ, start_response):
        req = Request(environ)
        method  = req.method
        path = req.path
        handler, methods = self.routes.find_node(path)
        if method in methods:
            func = getattr(handler, method)
            func()
        print(handler)
        print(method)


    def route(self, method, route):
        def wrapper(cls):
            self.routes.add_node(route, method, cls)
            print(self.routes)
        return wrapper


