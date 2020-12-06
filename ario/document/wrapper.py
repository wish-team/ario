from functools import wraps
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from werkzeug.wrappers import Response
from itertools import groupby

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
from werkzeug.serving import run_simple
from werkzeug.middleware.shared_data import SharedDataMiddleware

list_of_documents = []


class DocumentSpec:
    def __init__(self, port, spec, debug):
        self.spec = f"{spec} Spec of APIs"
        self.port = f"For Port {port}"
        self.debug = debug
        self.handler = ""
        self.dict_document = None
        self.docs = Documentation([], debug, self.spec, self.port)
        self.function_name = None

    def add_doc(self):
        def wrapper(handler):
            self.function_name = handler.__name__
            document = handler.__doc__.replace(" ", "").replace("\t", "").split("\n")
            document = list(filter(None, document))
            dict_document = dict(s.split(":") for s in document)
            self.dict_document = dict_document
            spec = self.spec
            port = self.port
            self.docs.add_to_list(self.function_name, dict_document)

        return wrapper

    def merge(self, document_spec_obj):
        pass

    def return_list(self):
        spec_arr = [d for d in globals()['list_of_documents'] if d['spec'] == self.spec]

        return globals()['list_of_documents']

    @staticmethod
    def return_url():
        return SCRIPT_DIR
    # new_doc.docs = Documentation([], new_doc.debug, new_doc.spec, new_doc.port)
    # new_doc.docs.add_to_list(new_doc.function_name, new_doc.dict_document)


class Documentation:
    def __init__(self, documents_list, debug, spec, port):
        self.debug = debug
        self.documents_list = documents_list
        self.spec = spec
        self.port = port

    def add_to_list(self, method, docs):
        arr = {'spec': self.spec, 'port': self.port, 'method': method, 'document': docs}
        list = []
        globals()['list_of_documents'].append(arr)
        self.documents_list = globals()['list_of_documents']
        # print('LIST: ', globals()['list_of_documents'])

        # print(globals()['list_of_documents'])

        # Render(self.documents_list).run_document()


class RenderDocument:
    def __init__(self, list_of_docs):
        self.docs = list_of_docs

    @staticmethod
    def render(list_of_docs):
        # print(list_of_docs)
        __env = Environment(loader=FileSystemLoader(SCRIPT_DIR + "/templates"),
                            autoescape=select_autoescape(['html', 'xml']))
        template = __env.get_template("doc.html")

        return Response(template.render(list_of_docs=list_of_docs), mimetype='text/html')
