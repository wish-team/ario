from wsgiref.headers import Headers
from http.cookies import SimpleCookie

class Response(Headers):
    def __init__(self, start_response):
        __response_encoding = None
        __cookies = SimpleCookie()
        self.start_response = start_response


    @property
    def response_encoding(self):
        return self.__response_encoding


    @response_encoding.setter
    def response_encoding(self, v):
        self.__response_encoding = v


    @property
    def content_type(self):
        content_type = self.get('Content-Type')
        if content_type:
            return content_type.split(';')[0]
        return None


    @content_type.setter
    def content_type(self, v):
        if v is None:
            del self['Content-Type']
        else:
            self['Content-Type'] = '%s; charset=%s' % (v, self.response_encoding)



    def cookie(self, name, value, options=None):
        self.__cookies[name] = value
        if options:
            for (k, v) in options:
                self.__cookies[name][k] = v


    def encode_response(self, buff):
        if isinstance(buff, bytes):
            return buff
        if self.response_encoding:
            return buff.encode(self.__response_encoding)
        return buff
