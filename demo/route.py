import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ario import RouterController, Endpoint 

control = RouterController()

@control.route(method=["GET"], route="/user")
class UserEndpoint(Endpoint):
    pass
