import json


class APIClientError(Exception):
    def __init__(self, **kwargs):
        self.attrs = kwargs.keys()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        Exception.__init__(self, str(kwargs))

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


class ServerError(APIClientError):
    pass


class ServiceUnavailableError(APIClientError):
    pass


class ServerTimeoutError(APIClientError):
    pass
