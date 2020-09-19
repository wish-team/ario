![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
# Ario - Python Lightweight Micro Framework
 > flask-based framework which is working with jinja2 and wrekzeug

This framework has been developed by Wish Team for web development purpose. This project is maintained by this team and hope make web development easier and faster.

## Motivation

The main concept of this framework is like flask. but it's only work like a dispatcher and you could easily use any library you want. you are not dependant to any 3rd specific libraries and also you do not have any regex in matching for your url which may cause ReDos to your system. you could specify the result of your response with just a decorator like ```@html``` or ```@jinja``` which is help for focusing on your development only.

## Instalation
Install and update using pip:

```
pip install ario
```

## Usage
First of all you should import classes that you want. ```RouterController, Endpoint, Application ``` should be imported and ```json, html, setup_jinja, jinja, redirect, forbidden, ok``` are arbitrary. 

```python
from werkzeug.serving import run_simple
from werkzeug.middleware.shared_data import SharedDataMiddleware
from ario import RouterController, Endpoint, Application, json, jinja2
from ario.status import forbidden, ok
```
For seting up your template:
```
setup_jinja("./templates")
```
For instance if we want to define two endpoint that one of them is json and the latter is jinja, we should define them as below:
```python
control = RouterController(debug=True)

@control.route(method=["GET", "POST", "HEAD"], route="/")
class DashboardEndpoint(Endpoint):
    @json
    def get(request, response):
        data = {
            "name": "john",
            "family_name": "doe",
            "age": 21,
            "phonenumber": "12345678"
        }
        return data
@control.route(method=["GET", "POST"], route="/user/$id")
class DashboardEndpoint(Endpoint):
    @jinja("base.html")
    def get(request, response, id):
        params = {"my_string": id, "my_list": [0, 1, 2]}
        return params
```
remeber for using jinja decorator, you should insert a ```base.html``` file in ```template``` folder
After all, we make a socket to our port use ```werkzeug```:
```python
if __name__ == '__main__':
    app = Application(control)
    app = SharedDataMiddleware(app, {
        '/static': os.path.join(os.path.dirname(__file__), 'templates/static')
    })
    print('Demo server started http://localhost:5000')
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
```
You could run your code easily by just typing ```python yourfile.py```

