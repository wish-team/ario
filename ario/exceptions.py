from ario.status import bad_request, unauthorized, forbidden, not_found

class Error(Exception):
    handler = None
    def __init__(self, message=None, status=None):
        self.status = status
        self.message = message
        super().__init__(message)


class BadRequestError(Error):
    def __init__(self, message="Bad Request", status=bad_request()):
        self.status = status
        self.message = message
        super().__init__(message, status)


class UnauthorizedError(Error):
    def __init__(self, message="Unauthorized", status=unauthorized()):
        self.status = status
        self.message = message
        super().__init__(message, status)


class ForbidenError(Error):
    def __init__(self, message="Forbiden", status=forbidden()):
        self.status = status
        self.message = message
        super().__init__(message, status)


class NotFoundError(Error):
    def __init__(self, message="Not Found", status=not_found()):
        self.status = status
        self.message = message
        super().__init__(message, status)


