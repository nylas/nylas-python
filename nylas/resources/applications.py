from nylas.handler.http_client import HttpClient
from nylas.models.application_details import ApplicationDetails
from nylas.models.response import Response
from nylas.resources.redirect_uris import RedirectUris
from nylas.resources.resource import Resource


class Applications(Resource):
    @property
    def redirect_uris(self) -> RedirectUris:
        return RedirectUris(self._http_client)

    def info(self) -> Response[ApplicationDetails]:
        """
        Get the application information.

        Returns:
            Response: The application information.
        """

        json_response = self._http_client._execute(
            method="GET", path="/v3/applications"
        )
        return Response.from_dict(json_response, ApplicationDetails)
