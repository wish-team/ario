import os
import mimetypes
from ario.exceptions import BadRequestError

SIZE = 1024 * 5

def serve_static(path, response):
    if not os.path.exists(path):
        raise BadRequestError()
    content_length  = os.path.getsize(path)
    content_type    = mimetypes.guess_type(path)[0]
    response.content_type = content_type
    response.content_length = content_length
    response.is_chunked = True
    def chunk_return():
        with open(path, 'rb') as file:
            while True:
                part = file.read(SIZE)
                if not part:
                    break
                yield part
    return chunk_return
