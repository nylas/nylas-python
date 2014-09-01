import json

class APIClientError(Exception):
    def __init__(self, **kwargs):
        self.attrs = kwargs.keys()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        Exception.__init__(self, str(kwargs))

    def __str__(self):
        resp = {}
        for attr in self.attrs:
            resp[attr] = getattr(self, attr)
        return json.dumps(resp)

class ConnectionError(APIClientError):
    pass


class NotAuthorizedError(APIClientError):
    pass


class APIError(APIClientError):
    pass


class ConflictError(APIClientError):
    pass


class NotFoundError(APIClientError):
    pass
