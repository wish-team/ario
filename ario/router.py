from dataclasses import dataclass
from typing import List
from ario.request import Request
from ario.response import Response
from ario.status import bad_request
from inspect import signature
from ario.exceptions import Error
import traceback
import json


@dataclass
class Endpoint:
    method: List[str]
    route: str

    def __call__(self):
        print(f"{self.route} called with {self.method}")
        print('ROUTE: ', self.route)

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

    def __init__(self, debug=False, langs=[]):
        if RouterController.__instance is None:
            self.__langs = langs
            self.routes = RouteNode([], "/", None)
            self.debug = debug
            RouterController.__instance = self
        else:
            raise Exception("Controller already instantiated")


    def __find_language(self, path):
        path = path.replace("/", "", 1)
        tokens = path.split("/")
        if tokens[0] in self.__langs:
            return tokens[0]
        return None


    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = Response(start_response)
        try:
            method = req.method
            path = req.path

            # in case of /{lang}/other the {lang} is removed and set as an
            # attribute in request and /other is processed as the path
            lang = self.__find_language(path)
            req.lang = lang
            if lang:
                if path == '/' + lang:
                    path = '/'
                else:
                    path = path[len(lang) + 1:]

            handler, methods, arg = self.routes.find_node(path)
            if methods is None or handler is None:
                ret = self.routes.default(req, resp)
            elif method in methods:
                func = getattr(handler, method)
                if arg and len(signature(func).parameters) == 3:
                    ret = func(req, resp, arg)
                else:
                    ret = func(req, resp)
            else:
                ret = self.routes.default(req, resp)
            resp.start()
            if resp.is_chunked:
                return ret()
            ret = resp.encode_response(ret)
            return iter([ret])
        except Error as ex:
            resp.content_type = 'text/html'
            if ex.handler is not None:
                ret = ex.handler()
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
