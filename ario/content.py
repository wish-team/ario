from functools import wraps
from status import moved_permanently
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
            response.status = moved_permanently()
            response.location = url
            return b'301 Moved Permanently' 
        return wrapper
    return decorator
