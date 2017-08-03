import json


class APIClientError(Exception):
    def __init__(self, **kwargs):
        if 'message' in kwargs:
            Exception.__init__(self, kwargs['message'])
        else:
            Exception.__init__(self, '')

        self.attrs = kwargs.keys()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def as_dict(self):
        resp = {}
        for attr in self.attrs:
            resp[attr] = getattr(self, attr)
        return resp

    def __str__(self):
        return json.dumps(self.as_dict())


class ConnectionError(APIClientError):
    pass


class NotAuthorizedError(APIClientError):
    pass


class InvalidRequestError(APIClientError):
    pass


class MessageRejectedError(APIClientError):
    pass


class ConflictError(APIClientError):
    pass


class SendingQuotaExceededError(APIClientError):
    pass


class NotFoundError(APIClientError):
    pass


class MethodNotSupportedError(APIClientError):
    pass


class ServerError(APIClientError):
    pass


class ServiceUnavailableError(APIClientError):
    pass


class ServerTimeoutError(APIClientError):
    pass


class FileUploadError(APIClientError):
    pass


STATUS_MAP = {
    400: InvalidRequestError,
    401: NotAuthorizedError,
    402: MessageRejectedError,
    403: NotAuthorizedError,
    404: NotFoundError,
    405: MethodNotSupportedError,
    409: ConflictError,
    429: SendingQuotaExceededError,
    500: ServerError,
    503: ServiceUnavailableError,
    504: ServerTimeoutError,
}
