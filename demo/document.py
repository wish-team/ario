from route import app
from run import app_2
from werkzeug.serving import run_simple
import os, sys
from ario.document import RenderDocument
from ario import Application, RouterController
from werkzeug.wrappers import Request, Response

PACKAGE_PARENT = '..'

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from werkzeug.middleware.shared_data import SharedDataMiddleware

document = app.merge(app_2)

RenderDocument.wsgi_app_render(document, port=9000)
