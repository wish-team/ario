from wsgiref.headers import Headers
from http.cookies import SimpleCookie
from ario.status import moved_temporarily, moved_permanently


class Response(Headers):
    def __init__(self, start_response):
        super().__init__()
        self.__response_encoding = "utf-8"
        self.__cookies = SimpleCookie()
        self.start_response = start_response
        self['Status'] = '200 OK'

    @property
    def response_encoding(self):
        return self.__response_encoding

    @response_encoding.setter
    def response_encoding(self, v):
        self.__response_encoding = v

    @property
    def status(self):
        return self['Status']

    @status.setter
    def status(self, v):
        if v is None:
            return
        self['Status'] = v.__str__()

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

    @property
    def location(self):
        location = self.get('Location')
        if location:
            return location
        return None

    @location.setter
    def location(self, v):
        if v is None:
            del self['Location']
        else:
            self['Location'] = v

    def perm_redirect(self, location):
        self.location = location
        self.status = moved_permanently()
        self.start()

    def temp_redirect(self, location):
        self.location = location
        self.status = moved_temporarily()
        self.start()

    def cookie(self, name, value, options=None):
        self.__cookies[name] = value
        if options:
            for k, v in options.items():
                self.__cookies[name][k] = v
        return self

    def encode_response(self, buff):
        if isinstance(buff, bytes):
            return buff
        if self.response_encoding:
            return buff.encode(self.__response_encoding)
        return buff

    def start(self):
        cookie = self.__cookies.output()
        if cookie:
            for line in cookie.split('\r\n'):
                print(line)
                print(line.split(': '))
                self.add_header(*line.split(': '))
        self.start_response(self.status, self.items())
