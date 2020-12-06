import os
import sys
from werkzeug.middleware.shared_data import SharedDataMiddleware
from wsgiref.simple_server import make_server
from werkzeug.serving import run_simple

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
PACKAGE_PARENT = '..'
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from ario import RouterController, Endpoint, Application, jinja, setup_jinja, html, json
from ario.document import Documentation, DocumentSpec

from ario.status import forbidden

documentation = DocumentSpec(port="5002", spec="run.py", debug=True)
control = RouterController(debug=True)
setup_jinja("./templates")


@control.route(method=["GET", "POST"], route="/usersss/$id")
class DashboardEndpoint(Endpoint):
    @documentation.add_doc()
    @json
    def get(request, response, id):
        """
        format: BN
        title: post to db

        user: XA
        password: 222
        """
        # print(id)
        params = {"my_string": id, "my_list": [0, 1, 2]}
        return params


app_2 = documentation
