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


