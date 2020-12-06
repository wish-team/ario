class API(object):
    def __init__(self, app=None, version="1.0", title=None,
                 default_mediatype='application/json', default_label='Default namespace'):
        self.app = app
        self.version = version
        self.title = title
        self.default_mediatype = default_mediatype
        self.default_label = default_label

    def error_handler(self, exception):
        '''A decorator to register an error handler for a given exception'''
