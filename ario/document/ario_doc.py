from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from werkzeug.wrappers import Response
from ario import Application
from werkzeug.serving import run_simple
from werkzeug.middleware.shared_data import SharedDataMiddleware
from itertools import groupby

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))

list_of_documents = []


class DocumentSpec:
    def __init__(self, port, spec, description, debug):
        self.spec = f"{spec} Spec of APIs"
        self.port = f"For Port {port}"
        self.description = description
        self.debug = debug
        self.handler = ""
        self.dict_document = None
        self.route = None
        self.docs = Documentation([], debug, self.spec, self.port, self.description)
        self.function_name = None

    def add_doc(self, route=None):
        self.route = route

        def wrapper(handler):
            self.function_name = handler.__name__
            document = handler.__doc__.replace("  ", "").replace("\t", "").split("\n")
            document = list(filter(None, document))

            print(document)
            dict_document = dict(s.split(":") for s in document)
            self.dict_document = dict_document
            spec = self.spec
            port = self.port
            self.docs.add_to_list(self.route, self.function_name, dict_document)

        return wrapper

    def merge(self, *args, **kwargs):
        field_to_be_check = "spec"
        field_to_be_check_2 = "port"
        field_to_be_check_3 = "description"
        primary = "general"
        merge_name = 'specific'
        grp = groupby(globals()['list_of_documents'],
                      key=lambda x: [x[field_to_be_check], x[field_to_be_check_2], x[field_to_be_check_3]])
        result = []

        for model, group in grp:
            func_dict = {}
            func_dict[primary] = model
            group_list = list(group)
            func_dict[merge_name] = []
            for item in group_list:
                item_set = {'route': item['route'], 'method': item['method'], 'document': item['document']}
                func_dict[merge_name].append(item_set)

            result.append(func_dict)
        return result

    def return_list(self):
        return globals()['list_of_documents']


class Documentation:
    def __init__(self, documents_list, debug, spec, port, description):
        self.debug = debug
        self.documents_list = documents_list
        self.spec = spec
        self.port = port
        self.description = description

    def add_to_list(self, route, method, docs):
        arr = {'spec': self.spec, 'port': self.port, 'route': route, 'description': self.description, 'method': method,
               'document': docs}
        globals()['list_of_documents'].append(arr)
        self.documents_list = globals()['list_of_documents']


class RenderDocument:
    def __init__(self, list_of_docs):
        self.docs = list_of_docs

    @staticmethod
    def render(list_of_docs):
        __env = Environment(loader=FileSystemLoader(SCRIPT_DIR + "/templates"),
                            autoescape=select_autoescape(['html', 'xml']))
        template = __env.get_template("doc.html")

        return Response(template.render(list_of_docs=list_of_docs), mimetype='text/html')

    @staticmethod
    def wsgi_app_render(document, **kwargs):
        if 'port' in kwargs:
            port = kwargs['port']
        else:
            port = 8888
        url = SCRIPT_DIR
        app = Application(RenderDocument.render(document))
        app = SharedDataMiddleware(app, {
            '/static': os.path.join(url, 'templates/static')
        })
        print(f'Ario Document Server started http://localhost:{port}')
        run_simple('127.0.0.1', port, app, use_debugger=True, use_reloader=True)
