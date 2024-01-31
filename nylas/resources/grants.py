from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.grants import (
    Grant,
    ListGrantsQueryParams,
    UpdateGrantRequest,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Grants(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    """
    Nylas Grants API

    The Grants API allows you to find and manage existing grants for your Nylas application.

    Grants represent a specific set of permissions ("scopes") that a specific end user granted Nylas
    for a specific service provider
    """

    def list(self, query_params: ListGrantsQueryParams = None) -> ListResponse[Grant]:
        """
        Return all Grants.

        Args:
            query_params: The query parameters to include in the request.

        Returns:
            A list of Grants.
        """

        return super().list(
            path="/v3/grants", response_type=Grant, query_params=query_params
        )

    def find(self, grant_id: str) -> Response[Grant]:
        """
        Return a Grant.

        Args:
            grant_id: The ID of the Grant to retrieve.

        Returns:
            The Grant.
        """

        return super().find(path=f"/v3/grants/{grant_id}", response_type=Grant)

    def update(
        self, grant_id: str, request_body: UpdateGrantRequest
    ) -> Response[Grant]:
        """
        Update a Grant.

        Args:
            grant_id: The ID of the Grant to update.
            request_body: The values to update the Grant with.

        Returns:
            The updated Grant.
        """

        return super().update(
            path=f"/v3/grants/{grant_id}",
            response_type=Grant,
            request_body=request_body,
        )

    def destroy(self, grant_id: str) -> DeleteResponse:
        """
        Delete a Grant.

        Args:
            grant_id: The ID of the Grant to delete.

        Returns:
            The deletion response.
        """

        return super().destroy(path=f"/v3/grants/{grant_id}")
