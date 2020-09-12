from functools import wraps
from ario.status import moved_temporarily
import ujson


def json(handler):
    @wraps(handler)
    def wrapper(request, response, *args):
        response.content_type = 'application/json'
        response.response_encoding = 'utf-8'
        body = handler(request, response, *args)
        body = ujson.dumps(body)
        body = response.encode_response(body)
        return body
    return wrapper


def html(handler):
    @wraps(handler)
    def wrapper(request, response, *args):
        response.content_type = 'text/html'
        response.response_encoding = 'utf-8'
        body = handler(request, response, *args)
        body = response.encode_response(body)
        return body
    return wrapper


def redirect(url):
    def decorator(handler):
        @wraps(handler)
        def wrapper(request, response):
            response.status = moved_temporarily()
            response.location = url
            response.start()
            return b'302 Moved Temporarily' 
        return wrapper
    return decorator
