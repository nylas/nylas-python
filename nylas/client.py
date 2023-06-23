from nylas.config import DEFAULT_SERVER_URL
from nylas.handler.http_client import HttpClient


class Client(object):
    """API client for the Nylas API."""

    def __init__(
        self, api_key: str, api_server: str = DEFAULT_SERVER_URL, timeout: int = 30
    ):
        self.api_key = api_key
        self.api_server = api_server
        self.http_client = HttpClient(self.api_server, self.api_key, timeout)

