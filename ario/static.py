from mimetypes import guess_type
from os import path
from ario.status import not_found

CHUNK_SIZE = 1024 * 10


def file(file_name):
    length = path.getsize(file_name)
    type_ = guess_type(path.split(file_name)[1])[0]
    print(type)

    def get(request):
        resp = request.response
        resp.length = length
        resp.type = type_
        with open(file_name, 'rb') as f:
            while True:
                chuck = f.read(CHUNK_SIZE)
                if not chuck:
                    break

                yield chuck

    return get


def dictionary(root_path):
    def get(request, location):
        resp = request.response
        file_name = path.join(root_path, location)

        if not path.exists(file_name):
            resp.status = not_found()
        resp.length = path.getsize(file_name)
        resp.type = guess_type(path.split(file_name)[1])[0]

        with open(file_name, 'rb') as f:
            while True:
                chunck = f.read(CHUNK_SIZE)
                if not chunck:
                    break

                yield chunck
        return get
