from nylas.config import RequestOverrides
from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.redirect_uri import (
    RedirectUri,
    CreateRedirectUriRequest,
    UpdateRedirectUriRequest,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class RedirectUris(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Manage Redirect URIs for your Nylas Application.

    These endpoints allow you to create, update, and delete Redirect URIs for your Nylas Application.
    """

    def list(self, overrides: RequestOverrides = None) -> ListResponse[RedirectUri]:
        """
        Return all Redirect URIs.

        Args:
            overrides: The request overrides to apply to the request.

        Returns:
            The list of Redirect URIs.
        """

        return super().list(
            path="/v3/applications/redirect-uris",
            response_type=RedirectUri,
            overrides=overrides,
        )

    def find(
        self, redirect_uri_id: str, overrides: RequestOverrides = None
    ) -> Response[RedirectUri]:
        """
        Return a Redirect URI.

        Args:
            redirect_uri_id: The ID of the Redirect URI to retrieve.
            overrides: The request overrides to apply to the request.

        Returns:
            The Redirect URI.
        """

        return super().find(
            path=f"/v3/applications/redirect-uris/{redirect_uri_id}",
            response_type=RedirectUri,
            overrides=overrides,
        )

    def create(
        self, request_body: CreateRedirectUriRequest, overrides: RequestOverrides = None
    ) -> Response[RedirectUri]:
        """
        Create a Redirect URI.

        Args:
            request_body: The values to create the Redirect URI with.
            overrides: The request overrides to apply to the request.

        Returns:
            The created Redirect URI.
        """

        return super().create(
            path="/v3/applications/redirect-uris",
            request_body=request_body,
            response_type=RedirectUri,
            overrides=overrides,
        )

    def update(
        self,
        redirect_uri_id: str,
        request_body: UpdateRedirectUriRequest,
        overrides: RequestOverrides = None,
    ) -> Response[RedirectUri]:
        """
        Update a Redirect URI.

        Args:
            redirect_uri_id: The ID of the Redirect URI to update.
            request_body: The values to update the Redirect URI with.
            overrides: The request overrides to apply to the request.

        Returns:
            The updated Redirect URI.
        """

        return super().update(
            path=f"/v3/applications/redirect-uris/{redirect_uri_id}",
            request_body=request_body,
            response_type=RedirectUri,
            overrides=overrides,
        )

    def destroy(
        self, redirect_uri_id: str, overrides: RequestOverrides = None
    ) -> DeleteResponse:
        """
        Delete a Redirect URI.

        Args:
            redirect_uri_id: The ID of the Redirect URI to delete.
            overrides: The request overrides to apply to the request.

        Returns:
            The deletion response.
        """

        return super().destroy(
            path=f"/v3/applications/redirect-uris/{redirect_uri_id}",
            overrides=overrides,
        )
