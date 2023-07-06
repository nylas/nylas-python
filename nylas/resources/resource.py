from nylas.handler.http_client import HttpClient


class Resource(object):
    def __init__(self, resource_name: str, http_client: HttpClient):
        self.resource_name = resource_name
        self._http_client = http_client
