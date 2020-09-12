from functools import wraps
from ario.status import moved_temporarily, moved_permanently
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


def redirect(url, perm=False):
    def decorator(handler):
        @wraps(handler)
        def wrapper(request, response, *args):
            ret = None
            if not perm:
                response.status = moved_temporarily()
                ret = b'302 Moved Temporarily' 
            else:
                response.status = moved_permanently()
                ret = b'301 Moved Permanently' 
            response.location = url
            response.start()
            return ret
        return wrapper
    return decorator
