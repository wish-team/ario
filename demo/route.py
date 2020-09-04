import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ario import RouterController, Endpoint, Application

control = RouterController()

@control.route(method=["GET", "PUT"], route="/user")
class UserEndpoint(Endpoint):
    pass


@control.route(method=["GET", "POST"], route="/dashboard/baz")
class DashboardEndpoint(Endpoint):
    pass


@control.route(method=["GET", "POST"], route="/user/test")
class DashboardEndpoint(Endpoint):
    pass

app = Application(control)
