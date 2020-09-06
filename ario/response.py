from wsgiref.headers import Headers

class Response(Headers):
    __response_encoding = None

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


    def encode_response(self, buff):
        if isinstance(buff, bytes):
            return buff
        if self.response_encoding:
            return buff.encode(self.__response_encoding)
        return buff
