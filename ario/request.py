class Lazy:
    __slots__ = ('f', )
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, t=None):
        f = self.f
        if obj is None:
            return f
        val = f(obj)
        setattr(obj, f.__name__, val)
        return val


class Request: 
    def __init__(self, environ):
        self.environ = environ


    @Lazy
    def content_length(self):
        return self.environ.get("CONTENT_LENGTH")


    @Lazy
    def method(self):
        return self.environ['REQUEST_METHOD'].lower()


    @Lazy
    def path(self):
        return self.environ['PATH_INFO'].lower()
