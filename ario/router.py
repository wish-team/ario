from dataclasses import dataclass
from typing import List
from ario.request import Request
from ario.response import Response
from ario.status import bad_request
from inspect import signature
from ario.exceptions import BadRequestError
import traceback


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
    def __init__(self, method, path, handler=None, child=[]):
        self.method = method
        self.path = path
        self.handler = handler
        self.child = child

    def add_node(self, route, method, handler):
        method = [m.lower() for m in method]
        tokens = RouteNode.__tokenize_route(route)
        if route == "/":
            self.method = method
            self.handler = handler
            return
        routes = self.child
        for i in range(len(tokens)):
            if len(routes) == 0:
                if len(tokens) - 1 == i:
                    node = RouteNode(method, tokens[i], handler, [])
                    if tokens[i][0] == "$":
                        routes.append(node)
                        routes = node.child
                    else:
                        routes.insert(0, node)
                        routes = node.child
                else:
                    node = RouteNode([], tokens[i], [], [])
                    routes.append(node)
                    routes = node.child
                continue
            for (j, r) in enumerate(routes):
                if r.path != tokens[i]:
                    if j == len(routes) - 1:
                        if len(tokens) - 1 == i:
                            node = RouteNode(method, tokens[i], handler, [])
                            if tokens[i][0] == "$":
                                routes.append(node)
                                routes = node.child
                            else:
                                routes.insert(0, node)
                                routes = node.child
                        else:
                            node = RouteNode([], tokens[i], [], [])
                            routes.append(node)
                            routes = node.child
                    continue
                if len(tokens) - 1 == i:
                    r.method = method
                    r.handdler = handler
                else:
                    routes = r.child
                break

    def add_default_node(self, handler):
        self.default = handler

    def find_node(self, route):
        tokens = RouteNode.__tokenize_route(route)
        if route == self.path:
            return (self.handler, self.method, None)
        routes = self.child
        args = None
        for i in range(len(tokens)):
            match_flag = False
            for (j, r) in enumerate(routes):
                if r.path != tokens[i]:
                    if len(tokens) - 1 == i and r.path[0] == '$':
                        return (r.handler, r.method, tokens[i])
                    continue
                match_flag = True
                if len(tokens) - 1 == i:
                    return (r.handler, r.method, None)
                else:
                    routes = r.child
                break
            if not match_flag:
                return None, None, None

    @staticmethod
    def __tokenize_route(route):
        route = route.replace("/", "", 1)
        tokens = route.split("/")
        return tokens

    def __repr__(self):
        return f"path: {self.path}, methods: {self.method}, \n child: {self.child} \n"


class RouterController:
    __instance = None

    @staticmethod
    def get_instance():
        if RouterController.__instance is None:
            RouterController()
        return RouterController.__instance

    def __init__(self, debug=False):
        if RouterController.__instance is None:
            self.routes = RouteNode([], "/", None)
            self.debug = debug
            RouterController.__instance = self
        else:
            raise Exception("Controller already instantiated")

    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = Response(start_response)
        try:
            method = req.method
            path = req.path
            handler, methods, arg = self.routes.find_node(path)
            if methods is None or handler is None:
                ret = self.routes.default(req, resp)
            elif method in methods:
                req = Request(environ)
                func = getattr(handler, method)
                if arg and len(signature(func).parameters) == 3:
                    ret = func(req, resp, arg)
                else:
                    ret = func(req, resp)
            else:
                ret = self.routes.default(req, resp)
            resp.start()
            return iter([ret])
        except BadRequestError as ex:
            if BadRequestError.handler is not None:
                ret = BadRequestError.handler()
                resp.start()
            else:
                ret = str(ex.status)
                ret = resp.encode_response(ret)
                resp.start()
            return iter([ret])
        except Exception as ex:
            if self.debug:
                tb = traceback.format_exc()
                tb = resp.encode_response(tb)
                resp.start()
                return iter([tb])
            else:
                ret = self.routes.default(req, resp)
                resp.start()
                return iter([ret])

    def route(self, method=[], route=None):
        def wrapper(handler):
            self.routes.add_node(route, method, handler)

        return wrapper

    def default(self):
        def wrapper(handler):
            self.routes.add_default_node(handler)

        return wrapper
