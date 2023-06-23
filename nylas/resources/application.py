from nylas.handler.http_client import HttpClient
from nylas.model.response import Response
from nylas.resources.redirect_uris import RedirectUris
from nylas.resources.resource import Resource


class Application(Resource):
    def __init__(self, http_client: HttpClient):
        super(Application, self).__init__("auth", http_client)

    @property
    def redirect_uris(self) -> RedirectUris:
        return RedirectUris(self._http_client)

    def info(self) -> Response:
        """Get the application information.

        Returns:
            Response: The application information.
        """

        json_response = self._http_client.get("/v3/applications")
        return Response.from_dict(json_response)
