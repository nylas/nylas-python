from nylas.models.application_details import ApplicationDetails
from nylas.models.response import Response
from nylas.resources.redirect_uris import RedirectUris
from nylas.resources.resource import Resource


class Applications(Resource):
    """
    Nylas Applications API

    The Nylas Applications API allows you to get information about your Nylas application.
    You can also manage the redirect URIs associated with your application.
    """

    @property
    def redirect_uris(self) -> RedirectUris:
        """
        Manage Redirect URIs for your Nylas Application.

        Returns:
            RedirectUris: The redirect URIs associated with your Nylas Application.
        """
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
