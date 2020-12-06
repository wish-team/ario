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

app.merge(app_2)

document = app.return_list()

if __name__ == '__main__':
    url = app.return_url()
    app = Application(RenderDocument.render(document))
    app = SharedDataMiddleware(app, {
        '/static': os.path.join(url, 'templates/static')
    })
    print('Doc server started http://localhost:5001')
    run_simple('127.0.0.1', 5001, app, use_debugger=True, use_reloader=True)
