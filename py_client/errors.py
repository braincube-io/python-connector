"""The errors module contains custom errors."""

ERROR_CODE_STATUS = {
    400: '400 Bad Request',
    401: '401 Unauthorized',
    402: '402 Payment Required',
    403: '403 Forbidden',
    404: '404 Not Found',
    405: '405 Method Not Allowed',
    406: '406 Not Acceptable',
    407: '407 Proxy Authentication Required',
    408: '408 Request Timeout',
    409: '409 Conflict',
    410: '410 Gone',
    411: '411 Length Required',
    412: '412 Precondition Failed',
    413: '413 Payload Too Large',
    414: '414 URI Too Long',
    415: '415 Unsupported Media Type',
    416: '416 Range Not Satisfiable',
    417: '417 Expectation Failed',
    418: "418 I'm a teapot",
    421: '421 Misdirected Request',
    422: '422 Unprocessable Entity',
    423: '423 Locked',
    424: '424 Failed Dependency',
    425: '425 Too Early',
    426: '426 Upgrade Required',
    428: '428 Precondition Required',
    429: '429 Too Many Requests',
    431: '431 Request Header Fields Too Large',
    451: '451 Unavailable For Legal Reasons'
}


class RequestError(Exception):
    """Handles html request errors"""
    def __init__(self, code, message=""):
        """
        :param code: Code of the error.
        :type code: int
        :param message: Optional error message.
        :type message: string
        """
        message = "\n{}".format(message) if message else ""
        message = "{}{}".format(ERROR_CODE_STATUS.get(code,"{} Error".format(code)), message)
        super(RequestError, self).__init__(message)
