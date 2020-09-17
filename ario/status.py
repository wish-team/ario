from functools import partial


class StatusCode:
    def __init__(self, code, text):
        self.__code = code
        self.__text = text

    def __str__(self):
        return f"{self.__code} {self.__text}"

    def __repr__(self):
        return f"{self.__code} {self.__text}"


status = StatusCode

ok = partial(status, 200, "OK")

created = partial(status, 201, "CREATED")

accepted = partial(status, 202, "ACCEPTED")

non_authoritative_information = partial(status, 203, "NON AUTHORITATIVE INFORMATION")

no_content = partial(status, 204, "No Content")

reset_content = partial(status, 205, "Reset Content")

partial_content = partial(status, 206, "Partial Content")

multi_status = partial(status, 207, "Multi Status")

multiple_choices = partial(status, 300, "Multiple Choices")

moved_permanently = partial(status, 301, "Moved Permanently")

moved_temporarily = partial(status, 302, "Moved Temporarily")

see_other = partial(status, 303, "See Other")

not_modified = partial(status, 304, "Not Modified")

use_proxy = partial(status, 305, "Use Proxy")

temporary_redirect = partial(status, 307, "Temporary Redirect")

permanent_redirect = partial(status, 308, "Permanent Redirect")

bad_request = partial(status, 400, 'Bad Request')

unauthorized = partial(status, 401, 'Unauthorized')

forbidden = partial(status, 403, 'Forbidden')

not_found = partial(status, 404, 'Not Found')

method_not_allowed = partial(status, 405, 'Method Not Allowed')

conflict = partial(status, 409, 'Conflict')

gone = partial(status, 410, 'Gone')

precondition_failed = partial(status, 412, 'Precondition Failed')

internal_server_error = partial(status, 500, 'Internal Server Error')

bad_gateway = partial(status, 502, 'Bad Gateway')
