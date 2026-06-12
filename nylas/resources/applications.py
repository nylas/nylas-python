from nylas.config import RequestOverrides
from nylas.handler.api_resources import UpdatablePatchApiResource
from nylas.models.application_details import (
    ApplicationDetails,
    UpdateApplicationRequest,
)
from nylas.models.response import Response
from nylas.resources.redirect_uris import RedirectUris


class Applications(UpdatablePatchApiResource):
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

    def info(self, overrides: RequestOverrides = None) -> Response[ApplicationDetails]:
        """
        Get the application information.

        Args:
            overrides: The query parameters to include in the request.

        Returns:
            Response: The application information.
        """

        json_response, headers = self._http_client._execute(
            method="GET", path="/v3/applications", overrides=overrides
        )
        return Response.from_dict(json_response, ApplicationDetails, headers)

    def update(
        self,
        request_body: UpdateApplicationRequest,
        overrides: RequestOverrides = None,
    ) -> Response[ApplicationDetails]:
        """
        Update the application information.

        Note:
            ``additional_settings`` is write-only and is stripped from the response.

        Args:
            request_body: The values to update the application with.
            overrides: The request overrides to apply to the request.

        Returns:
            Response: The updated application information.
        """

        return super().patch(
            path="/v3/applications",
            request_body=request_body,
            response_type=ApplicationDetails,
            overrides=overrides,
        )
