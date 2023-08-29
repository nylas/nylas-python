from nylas.handler.http_client import HttpClient


class Resource(object):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
