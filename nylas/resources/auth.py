from nylas.handler.http_client import HttpClient
from nylas.resources.grants import Grants
from nylas.resources.providers import Providers
from nylas.resources.resource import Resource


class Auth(Resource):
    def __init__(self, http_client: HttpClient, client_id: str, client_secret: str):
        super(Auth, self).__init__("auth", http_client)
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def grants(self) -> Grants:
        return Grants(self._http_client)

    @property
    def providers(self) -> Providers:
        return Providers(self._http_client, self.client_id)
